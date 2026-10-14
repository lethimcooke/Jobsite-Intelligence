// Contact-form filler for Option A (user approves screenshots in chat before any submit).
//
// Usage (run from the repo root):
//   node scripts/fill_form.cjs <spec.json> <out_dir>            fill + screenshot, never submits
//   node scripts/fill_form.cjs <spec.json> <out_dir> --submit   fill, submit, screenshot the result
//
// spec.json: {
//   "id": "T1-F2", "url": "https://...",
//   "fields": [ {"selector": "input[name=email]", "value": "..."} ],
//   "selects": [ {"selector": "select", "label": "Other"} ],      (optional)
//   "submit": "button[type=submit]",                              (needed for --submit)
//   "success_text": ["thank", "received"]                         (optional, lowercase)
// }
// Stops without submitting when a CAPTCHA or a no-solicitation notice is found.
// Writes <id>_filled.png (and <id>_confirmation.png + <id>_result.json on submit).
// result.submitted is true only when a success message shows and no CAPTCHA appeared after the click.
const path = require('path');
const fs = require('fs');
const { chromium } = require(path.join(__dirname, '..', 'jobsite-report', 'node_modules', 'playwright'));

const CAPTCHA = '.g-recaptcha,iframe[src*="recaptcha"],iframe[src*="hcaptcha"],iframe[src*="turnstile"],.cf-turnstile,[data-sitekey],input[name="_wpcf7_recaptcha_response"]';
const NO_SOLICIT = /no solicit|do not solicit|solicitations? (are|is) not|not accept(ing)? solicit/;

(async () => {
  const [specPath, outDir, flag] = process.argv.slice(2);
  if (!specPath || !outDir) { console.error('usage: fill_form.cjs <spec.json> <out_dir> [--submit]'); process.exit(2); }
  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  const submit = flag === '--submit';
  fs.mkdirSync(outDir, { recursive: true });
  const launch = { executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] };
  if (process.env.HTTPS_PROXY) launch.proxy = { server: process.env.HTTPS_PROXY };
  const browser = await chromium.launch(launch);
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const result = { id: spec.id, url: spec.url, submitted: false, time: new Date().toISOString() };
  try {
    try { await page.goto(spec.url, { waitUntil: 'domcontentloaded', timeout: 45000 }); }
    catch (e) { console.log('load warning:', e.message.split('\n')[0]); }
    await page.waitForTimeout(6000);
    const checks = await page.evaluate(([cap]) => ({
      captcha: !!document.querySelector(cap),
      text: (document.body ? document.body.innerText : '').toLowerCase(),
    }), [CAPTCHA]);
    result.captcha = checks.captcha;
    result.no_solicit = NO_SOLICIT.test(checks.text);
    for (const f of spec.fields) {
      const el = page.locator(f.selector).first();
      await el.scrollIntoViewIfNeeded();
      await el.fill(f.value);
    }
    for (const s of spec.selects || []) await page.locator(s.selector).first().selectOption({ label: s.label });
    // Read back what is actually in each field, so the approval covers the full text.
    result.filled = [];
    for (const f of spec.fields) result.filled.push({ selector: f.selector, value: await page.locator(f.selector).first().inputValue() });
    result.filled_matches_spec = result.filled.every((x, i) => x.value === spec.fields[i].value);
    result.select_options = await page.evaluate(() => [...document.querySelectorAll('select')].map(e => [...e.options].map(o => o.textContent.trim())));
    const first = page.locator(spec.fields[0].selector).first();
    await first.scrollIntoViewIfNeeded();
    await page.screenshot({ path: path.join(outDir, `${spec.id}_filled.png`), fullPage: false });
    await page.screenshot({ path: path.join(outDir, `${spec.id}_filled_full.png`), fullPage: true });
    if (result.captcha || result.no_solicit) {
      result.blocked = result.captcha ? 'captcha' : 'no_solicit';
      console.log('BLOCKED:', result.blocked, '(manual or skip; not submitting)');
    } else if (submit) {
      if (!spec.submit) throw new Error('spec has no submit selector');
      await page.locator(spec.submit).first().click();
      await page.waitForTimeout(8000);
      const after = (await page.evaluate(() => document.body.innerText)).toLowerCase();
      // Some sites (Wix) only show a CAPTCHA after Submit is clicked; then nothing was sent.
      result.captcha_after_submit = await page.evaluate(([cap]) => !!document.querySelector(cap), [CAPTCHA]);
      result.clicked_submit = true;
      result.final_url = page.url();
      result.success_match = (spec.success_text || ['thank', 'received', 'sent']).filter(t => after.includes(t));
      // Only a visible success message counts as delivered; anything else is logged as not sent.
      result.submitted = !result.captcha_after_submit && result.success_match.length > 0;
      if (result.captcha_after_submit) { result.blocked = 'captcha_after_submit'; console.log('BLOCKED: CAPTCHA appeared on submit; nothing was sent (manual).'); }
      else if (!result.submitted) console.log('UNCONFIRMED: no success message; do not log as sent.');
      await page.screenshot({ path: path.join(outDir, `${spec.id}_confirmation.png`), fullPage: false });
      await page.screenshot({ path: path.join(outDir, `${spec.id}_confirmation_full.png`), fullPage: true });
    }
  } catch (e) {
    result.error = e.message.split('\n')[0];
  } finally {
    fs.writeFileSync(path.join(outDir, `${spec.id}_result.json`), JSON.stringify(result, null, 2));
    console.log(JSON.stringify(result));
    await browser.close();
  }
})();
