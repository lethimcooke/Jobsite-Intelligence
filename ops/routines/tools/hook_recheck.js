// Live re-check of Jobsite hooks by TCEQ authorization number. node hook_recheck.js <TXR15....> [...] > out.json
// Source: the five TCEQ Central Registry files on data.texas.gov (program STORM), the same the pull and the JSI
// publisher use. Per authorization: every operator row with its status and affiliation-begin ("record") date.
// hook_gate.py and the pre-send read this output (load_checked) as a saved re-check.
const FILES = ['msah-s2rv', '5eqq-7nad', 't34q-qzi3', 'tzyg-j7q4', '9iad-hrn8'];
(async () => {
  const out = { checked_at: new Date().toISOString(), records: {} };
  for (const id of process.argv.slice(2)) {
    const clean = id.replace(/[^A-Z0-9]/g, ''), where = encodeURIComponent(`program_code='STORM' AND additional_id_text='${clean}'`);
    const rows = []; let failed = 0;
    for (const ds of FILES) {
      try {
        const r = await fetch(`https://data.texas.gov/resource/${ds}.json?$select=ref_num_txt,reg_ent_name,re_phys_loc_addr_line_1,re_phys_loc_city,additional_id_status,affil_begin_dt,princ_name,name_txt&$limit=50&$where=${where}`);
        if (!r.ok) { failed++; continue; }
        for (const x of await r.json()) rows.push({ dataset: ds, rn: x.ref_num_txt, site: x.reg_ent_name, address: [x.re_phys_loc_addr_line_1, x.re_phys_loc_city].filter(Boolean).join(', '),
          status: x.additional_id_status || '', date: String(x.affil_begin_dt || '').slice(0, 10), operator: x.princ_name || '', operator_type: x.name_txt || '' });
      } catch (e) { failed++; }
    }
    out.records[clean] = !rows.length && failed ? { source: 'TCEQ Central Registry', unavailable: true, failed_files: failed }
      : { source: 'TCEQ Central Registry', rows, active: rows.some(x => /^ACTIVE$/i.test(x.status)), failed_files: failed };
  }
  console.log(JSON.stringify(out, null, 1));
})();
