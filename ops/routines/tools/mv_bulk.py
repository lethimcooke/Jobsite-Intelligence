"""MillionVerifier for Jobsite: website route only, one CSV shared with ASI (user, Nov 20).

python -I mv_bulk.py --repo . collect [--max 1000] [--outbox D:\\Workspace\\austin-signage-repo\\verify\\outbox]
        build a batch from addresses waiting for verification and append them to the shared outbox file
        <outbox>/<today>.csv (columns email,business; business JSI). The user uploads that file on the
        MillionVerifier website and saves the results file in D:\\Workspace\\austin-signage-repo\\verify\\inbox\\.
python -I mv_bulk.py --repo . import-shared RESULTS.csv [RESULTS.csv ...]
        import a combined ASI+JSI results file: only addresses in Jobsite's open batches are taken (ASI's rows
        are ignored); each batch with at least one address in the file is imported. Writes a marker
        <RESULTS>.jsi_imported.txt beside the file so ASI knows Jobsite is done with it (ASI moves it to done\\).
python -I mv_bulk.py --repo . import-inbox [--inbox D:\\Workspace\\austin-signage-repo\\verify\\inbox]
        import-shared every results file in the inbox and inbox\\done\\ that has no Jobsite marker yet.
python -I mv_bulk.py --repo . status

There is no API code here: the bulk API is off for both businesses (user, Nov 20) and this tool never reads,
prints or stores MILLIONVERIFIER_API_KEY. Nothing here sends email.

Pending = addresses in data/to_verify_<YYYY-MM-DD>*.csv (columns email, company, metro, site; the replenish writes
them with no copy) not already verified (data/verified_emails.csv or any older data/verified_*.csv), not on
do-not-contact (address or company domain), not in the send ledger, not in an open batch, and not "unknown" twice.
Import: ok -> "Deliverable"; catch_all -> "Risky: accept-all"; invalid/disposable -> "Undeliverable"; unknown ->
retried in the next batch once, then "Unknown". "(free mail)" is appended for free-mail domains. Copy is written
only for ok rows (and catch-all rows whose address is published on the hauler's own site), by the replenish.
"""
import argparse, csv, datetime, glob, io, json, os, re, sys

FREE = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "live.com", "icloud.com", "msn.com",
        "ymail.com", "att.net", "sbcglobal.net", "comcast.net", "verizon.net", "me.com", "protonmail.com"}
LABEL = {"ok": "Deliverable", "catch_all": "Risky: accept-all", "invalid": "Undeliverable",
         "disposable": "Undeliverable", "unknown": "Unknown"}
BUSINESS = "JSI"
SHARED = r"D:\Workspace\austin-signage-repo\verify"
VFIELDS = ["email", "company", "list", "metro", "service", "result", "checked_on"]


def read_csv(p):
    if not os.path.exists(p): return []
    with open(p, newline="", encoding="utf-8-sig") as fh: return list(csv.DictReader(fh))


def state_path(repo): return os.path.join(repo, "data", "verify_batches", "state.json")


def load_state(repo):
    p = state_path(repo)
    if not os.path.exists(p): return {"batches": []}
    with open(p, encoding="utf-8") as fh: return json.load(fh)


def save_state(repo, st):
    d = os.path.dirname(state_path(repo)); os.makedirs(d, exist_ok=True)
    tmp = state_path(repo) + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh: json.dump(st, fh, indent=1); fh.write("\n")
    os.replace(tmp, state_path(repo))


def verified(repo):
    out = set()
    for f in glob.glob(os.path.join(repo, "data", "verified_*.csv")):
        for r in read_csv(f):
            e = (r.get("email") or "").strip().lower()
            if e: out.add(e)
    return out


def pending(repo, st):
    data = os.path.join(repo, "data")
    dnc_rows = read_csv(os.path.join(data, "do_not_contact.csv"))
    dnc = {(r.get("email") or "").strip().lower() for r in dnc_rows}
    dnc_dom = {(r.get("domain") or "").strip().lower() for r in dnc_rows} - {""} - FREE
    contacted = {(r.get("to") or "").strip().lower() for r in read_csv(os.path.join(data, "send_ledger.csv"))}
    open_batch = {e for b in st["batches"] if not b.get("imported") for e in b.get("emails", [])}
    unknown_twice = {e for e, n in st.get("unknown_count", {}).items() if n >= 2}
    skip = verified(repo) | dnc | contacted | open_batch | unknown_twice
    out, seen = [], set()
    for f in sorted(glob.glob(os.path.join(data, "to_verify_*.csv"))):
        m = re.match(r"to_verify_(\d{4}-\d{2}-\d{2})", os.path.basename(f))
        if not m: continue                       # older undated files were verified by hand (data/verified_*.csv)
        for r in read_csv(f):
            e = (r.get("email") or "").strip().lower()
            if not e or "@" not in e or e in seen or e in skip or e.split("@")[1] in dnc_dom: continue
            seen.add(e)
            out.append({"email": e, "company": r.get("company", ""), "metro": r.get("metro", ""),
                        "site": r.get("site") or r.get("project") or "", "source": os.path.basename(f), "since": m.group(1)})
    out.sort(key=lambda x: x["since"])
    return out


def append_outbox(outbox, today, emails):
    """Append emails to <outbox>/<today>.csv (email,business), creating it with its header; addresses already in
    the file (either business) are not repeated. Returns how many rows were added."""
    os.makedirs(outbox, exist_ok=True)
    path = os.path.join(outbox, f"{today}.csv")
    have = {(r.get("email") or "").strip().lower() for r in read_csv(path)}
    new = [e for e in emails if e not in have]
    if not new: return 0, path
    exists = os.path.exists(path) and os.path.getsize(path) > 0
    with open(path, "a", newline="", encoding="utf-8") as fh:
        if exists:
            with open(path, "rb") as rf:
                rf.seek(-1, os.SEEK_END)
                if rf.read(1) not in (b"\n", b"\r"): fh.write("\n")
        else:
            fh.write("email,business\n")
        fh.write("".join(f"{e},{BUSINESS}\n" for e in new))
    return len(new), path


def cmd_collect(repo, mx, today, outbox):
    st = load_state(repo)
    # Website mode (user, Nov 24, as ASI): an open, unverified batch never blocks a new one. pending() already leaves
    # out addresses in open batches, so each collect takes only addresses not yet in any batch.
    rows = pending(repo, st)[:mx]
    if not rows:
        print("nothing pending verification"); return None
    bid = today
    if any(b["id"] == bid for b in st["batches"]):
        bid = f"{today}-{sum(1 for b in st['batches'] if b['id'].startswith(today)) + 1}"
    d = os.path.join(repo, "data", "verify_batches", bid); os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "batch.csv"), "w", newline="", encoding="utf-8") as fh:
        fh.write("email\n" + "".join(r["email"] + "\n" for r in rows))
    with open(os.path.join(d, "rows.json"), "w", encoding="utf-8", newline="\n") as fh: json.dump(rows, fh, indent=1)
    added, path = append_outbox(outbox, today, [r["email"] for r in rows])
    b = {"id": bid, "collected_at": today, "emails": [r["email"] for r in rows], "rows": len(rows), "outbox": path, "route": "web"}
    st["batches"].append(b); save_state(repo, st)
    print(f"batch {bid}: {len(rows)} addresses; {added} appended to {path} (business {BUSINESS})")
    print(f"Verify {path} on the MillionVerifier website and save the results file in {os.path.join(os.path.dirname(outbox), 'inbox')}.")
    return b


def parse_results(raw_text):
    out = {}
    for r in csv.DictReader(io.StringIO(raw_text)):
        low = {k.strip().lower(): (v or "").strip() for k, v in r.items() if k}
        e = (low.get("email") or "").lower()
        res = (low.get("result") or low.get("mv_result") or "").lower()
        if e and res: out[e] = (res, (low.get("business") or "").upper())
    return out


def cmd_import_shared(repo, path, today):
    with open(path, encoding="utf-8-sig") as fh: res = parse_results(fh.read())
    if not res: raise SystemExit(f"{path}: no email/result rows found")
    st = load_state(repo); uc = st.setdefault("unknown_count", {})
    vpath = os.path.join(repo, "data", "verified_emails.csv")
    have = {(r["email"].lower(), r["checked_on"]) for r in read_csv(vpath)}
    summary, done, new_rows = {}, [], []
    mine = set()
    for b in st["batches"]:
        if b.get("imported"): continue
        hits = [e for e in b["emails"] if e in res]
        if not hits: continue
        d = os.path.join(repo, "data", "verify_batches", b["id"])
        meta = {r["email"]: r for r in json.load(open(os.path.join(d, "rows.json"), encoding="utf-8"))}
        for e in hits:
            mine.add(e)
            r = res[e][0]
            summary[r] = summary.get(r, 0) + 1
            if r == "unknown":
                uc[e] = uc.get(e, 0) + 1
                if uc[e] < 2: continue                     # returns to pending once
            label = LABEL.get(r, "Unknown") + (" (free mail)" if e.split("@")[1] in FREE else "")
            m = meta.get(e, {})
            if (e, today) not in have:
                new_rows.append({"email": e, "company": m.get("company", ""), "list": m.get("source", ""), "metro": m.get("metro", ""),
                                 "service": "MillionVerifier (website)", "result": label, "checked_on": today})
                have.add((e, today))
        b["imported"] = today; b["results_file"] = os.path.basename(path)
        b["missing"] = len(b["emails"]) - len(hits)                # not in the file: they return to pending
        done.append(b["id"])
    if new_rows:
        exists = os.path.exists(vpath)
        with open(vpath, "a", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=VFIELDS, lineterminator="\n")
            if not exists: w.writeheader()
            w.writerows(new_rows)
    save_state(repo, st)
    ignored = len(res) - len(mine)
    with open(path + ".jsi_imported.txt", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(f"Jobsite imported {today}: batches {', '.join(done) or 'none'}; {len(mine)} Jobsite results "
                 f"{json.dumps(summary)}; {ignored} other rows ignored\n")
    print(f"{os.path.basename(path)}: {len(res)} results; Jobsite batches imported: {', '.join(done) or 'none'}; "
          f"ours {len(mine)} {json.dumps(summary)}; ignored {ignored}; {len(new_rows)} rows added to data/verified_emails.csv")
    return {"batches": done, "results": summary, "ignored": ignored, "added": len(new_rows)}


def inbox_files(inbox):
    files = []
    for d in (inbox, os.path.join(inbox, "done")):
        for f in sorted(glob.glob(os.path.join(d, "*.csv"))):
            if not os.path.exists(f + ".jsi_imported.txt"): files.append(f)
    return files


def cmd_status(repo):
    st = load_state(repo)
    for b in st["batches"]:
        print(b["id"], b["rows"], "imported " + b["imported"] if b.get("imported") else "waiting for website results", b.get("outbox", ""))
    print("pending now:", len(pending(repo, st)))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True); p.add_argument("--today", default=datetime.date.today().isoformat())
    p.add_argument("cmd", choices=["collect", "import-shared", "import-inbox", "status"])
    p.add_argument("files", nargs="*"); p.add_argument("--max", type=int, default=1000)
    p.add_argument("--outbox", default=os.path.join(SHARED, "outbox")); p.add_argument("--inbox", default=os.path.join(SHARED, "inbox"))
    a = p.parse_args()
    repo = os.path.abspath(a.repo)
    if a.cmd == "collect": cmd_collect(repo, a.max, a.today, a.outbox)
    elif a.cmd == "import-shared":
        if not a.files: sys.exit("import-shared needs at least one results file")
        for f in a.files: cmd_import_shared(repo, f, a.today)
    elif a.cmd == "import-inbox":
        fs = inbox_files(a.inbox)
        if not fs: print(f"no results files without a Jobsite marker in {a.inbox} or its done folder")
        for f in fs: cmd_import_shared(repo, f, a.today)
    else: cmd_status(repo)
