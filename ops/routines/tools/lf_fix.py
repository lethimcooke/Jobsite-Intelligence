"""Convert CRLF to LF in JSON files written by asi_ops.py / ji_ops.py on Windows, checking the JSON is unchanged.
python -I lf_fix.py <file or glob> [...]"""
import glob, json, sys
n = 0
for pat in sys.argv[1:]:
    for p in glob.glob(pat):
        b = open(p, "rb").read()
        if b"\r\n" not in b: continue
        nb = b.replace(b"\r\n", b"\n")
        assert json.loads(nb) == json.loads(b), p
        open(p, "wb").write(nb); n += 1; print("LF:", p)
print(f"{n} file(s) fixed")
