#!/usr/bin/env node
/*
 * Jobsite Intelligence PDF export (adapted from Austin Signage Intelligence's template).
 *
 * Loads index.html directly from disk (file://), injects report-data.json
 * (or a data file given as the first CLI argument) into the page
 * (sidestepping the fetch-over-file:// restriction that a plain
 * double-click preview runs into), waits for local Instrument Sans fonts
 * to finish loading, then prints a Letter-portrait PDF — one cover/
 * at-a-glance page, one page per two projects, and one pilot-offer page
 * (five pages for a standard five-project sample) — with backgrounds
 * intact and no browser-generated headers/footers.
 *
 * Usage: node export.js [path/to/data.json] [output-filename.pdf]
 * With no arguments, reads report-data.json and writes
 * jobsite-intelligence-sample-report-001.pdf (the default sample).
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = __dirname;
const DATA_PATH = path.resolve(ROOT, process.argv[2] || 'report-data.json');
const INDEX_PATH = path.join(ROOT, 'index.html');
const RENDERER_PATH = path.join(ROOT, 'render-report.js');
const EXPORT_DIR = path.join(ROOT, 'exports');
const OUT_NAME = process.argv[3] || 'jobsite-intelligence-sample-report-001.pdf';
const OUT_PATH = path.join(EXPORT_DIR, OUT_NAME);

const REQUIRED_FONTS = [
  'assets/fonts/instrument-sans-regular.woff2',
  'assets/fonts/instrument-sans-medium.woff2',
  'assets/fonts/instrument-sans-semibold.woff2',
  'assets/fonts/instrument-sans-bold.woff2',
];
const REQUIRED_ASSETS = ['assets/field-bracket.svg'];

// Line budget for the five labeled sections on every project card, as
// rendered in the PDF. Keeps every card the same shape and length:
// What's filed 2 lines, Likely sign work 2, Who decides 3, Contact 1,
// Suggested first step 1-2. The export fails if any section is off, so
// rewrite that field (shorter or fuller) rather than changing the layout.
const LINE_BUDGET = {
  whatsFiled:     { min: 2, max: 2, label: "What's filed" },
  likelyScope: { min: 2, max: 2, label: 'Likely hauling work (our read)' },
  whoDecides:     { min: 3, max: 3, label: "Who decides / what's unknown" },
  contactLine:    { min: 1, max: 1, label: 'Contact' },
  firstStep:      { min: 1, max: 2, label: 'Suggested first step' },
};

function launchOptionsFor(chromium) {
  // Normally Playwright resolves its own bundled Chromium (installed via
  // `npx playwright install`). Some sandboxes pre-install a browser cache
  // whose revision doesn't match the npm package's expected build; if the
  // default executable is missing, fall back to any chrome/chromium binary
  // found under PLAYWRIGHT_BROWSERS_PATH.
  try {
    const defaultPath = chromium.executablePath();
    if (defaultPath && fs.existsSync(defaultPath)) return {};
  } catch (e) {
    // fall through to search
  }
  const browsersDir = process.env.PLAYWRIGHT_BROWSERS_PATH;
  if (browsersDir && fs.existsSync(browsersDir)) {
    const candidates = fs.readdirSync(browsersDir)
      .filter((d) => /^chromium(?!.*headless_shell)/.test(d))
      .sort()
      .reverse();
    for (const dir of candidates) {
      const exe = path.join(browsersDir, dir, 'chrome-linux', 'chrome');
      if (fs.existsSync(exe)) return { executablePath: exe };
    }
  }
  return {};
}

function fail(message) {
  console.error('\n[export] FAILED: ' + message + '\n');
  process.exit(1);
}

function checkRequiredFiles() {
  const missing = [];
  for (const rel of [...REQUIRED_FONTS, ...REQUIRED_ASSETS]) {
    if (!fs.existsSync(path.join(ROOT, rel))) missing.push(rel);
  }
  if (!fs.existsSync(DATA_PATH)) missing.push('report-data.json');
  if (!fs.existsSync(INDEX_PATH)) missing.push('index.html');
  if (!fs.existsSync(RENDERER_PATH)) missing.push('render-report.js');
  if (missing.length) {
    fail('missing required file(s):\n  - ' + missing.join('\n  - '));
  }
}

function loadAndValidateData() {
  let data;
  try {
    data = JSON.parse(fs.readFileSync(DATA_PATH, 'utf8'));
  } catch (e) {
    fail('report-data.json is not valid JSON — ' + e.message);
  }
  // House style: no em dashes anywhere in a sample (user rule). Fail the export if one slips in.
  const raw = fs.readFileSync(DATA_PATH, 'utf8');
  const emDashes = (raw.match(/\u2014/g) || []).length;
  if (emDashes) {
    const ctx = raw.slice(Math.max(0, raw.indexOf('\u2014') - 60), raw.indexOf('\u2014') + 40).replace(/\n/g, ' ');
    fail(emDashes + ' em dash(es) in ' + path.basename(DATA_PATH) + '. House style forbids them; rewrite with a comma, colon, semicolon or period. First one: ...' + ctx + '...');
  }
  if (!Array.isArray(data.projects) || data.projects.length < 4 || data.projects.length > 6) {
    fail('data file must contain 4-6 entries in "projects" (found ' +
      (data.projects ? data.projects.length : 0) + ') — the report is built two-per-page across at most three project pages');
  }
  const requiredProjectFields = [
    'number', 'name', 'tag', 'address', 'area', 'filedStart', 'value',
    'recordLabel', 'recordUrl', 'whatsFiled', 'likelyScope', 'whoDecides',
    'contactLine', 'firstStep',
  ];
  data.projects.forEach((p, i) => {
    for (const field of requiredProjectFields) {
      if (!p[field]) fail(`project #${i + 1} ("${p.name || 'unnamed'}") is missing required field "${field}"`);
    }
    if (!/^(Roll-off|Portable toilets|Roll-off \+ portable toilets)$/.test(p.tag)) {
      fail(`project #${i + 1} ("${p.name}") has tag "${p.tag}" — must be exactly "Roll-off", "Portable toilets" or "Roll-off + portable toilets"`);
    }
  });
  for (const section of ['report', 'pilot', 'brand', 'meta']) {
    if (!data[section]) fail(`data file is missing required top-level section "${section}"`);
  }
  const expectedPageCount = 1 + Math.ceil(data.projects.length / 2) + 1;
  if (expectedPageCount > 5) {
    fail(`this many projects (${data.projects.length}) would produce ${expectedPageCount} pages — the report must stay at 5 pages maximum`);
  }
  data._expectedPageCount = expectedPageCount;
  return data;
}

async function run() {
  console.log('[export] Checking required files...');
  checkRequiredFiles();

  console.log('[export] Loading and validating report-data.json...');
  const data = loadAndValidateData();

  fs.mkdirSync(EXPORT_DIR, { recursive: true });

  console.log('[export] Launching headless Chromium...');
  const browser = await chromium.launch(launchOptionsFor(chromium));
  const page = await browser.newPage();

  try {
    const fileUrl = 'file://' + INDEX_PATH;
    console.log('[export] Loading ' + fileUrl);
    await page.goto(fileUrl, { waitUntil: 'load' });

    console.log('[export] Rendering report from data...');
    await page.evaluate((reportData) => {
      window.renderReport(reportData);
    }, data);

    await page.waitForSelector('#report-root[data-render-complete="true"]');

    // Defensive: the page's own fetch() against report-data.json always
    // fails under file:// (expected — export injects data directly instead)
    // and index.html guards against showing its error banner in that case,
    // but strip the element outright so a race can never leak a 9th page.
    await page.evaluate(() => {
      const err = document.getElementById('load-error');
      if (err) err.remove();
    });

    const pageCount = await page.evaluate(() => document.querySelectorAll('.page').length);
    if (pageCount !== data._expectedPageCount) {
      fail(`rendered ${pageCount} .page elements — expected exactly ${data._expectedPageCount}`);
    }
    console.log(`[export] Rendered ${pageCount} pages.`);

    console.log('[export] Waiting for fonts to finish loading...');
    await page.evaluate(async () => {
      if (document.fonts && document.fonts.ready) {
        await document.fonts.ready;
      }
    });

    // Give the layout a beat to settle after font swap before measuring/painting.
    await page.waitForTimeout(150);

    console.log('[export] Checking section line counts...');
    const lineCounts = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('.proj-card')).map((card) => ({
        project: card.getAttribute('data-project'),
        fields: Array.from(card.querySelectorAll('.pl-value[data-field]')).map((el) => {
          const lh = parseFloat(getComputedStyle(el).lineHeight);
          return { field: el.getAttribute('data-field'), lines: Math.round(el.getBoundingClientRect().height / lh) };
        }),
      }));
    });
    const lineErrors = [];
    for (const card of lineCounts) {
      for (const f of card.fields) {
        const rule = LINE_BUDGET[f.field];
        if (!rule) continue;
        if (f.lines < rule.min || f.lines > rule.max) {
          const want = rule.min === rule.max ? `${rule.min}` : `${rule.min}-${rule.max}`;
          lineErrors.push(`${card.project}: "${rule.label}" runs ${f.lines} line(s), needs ${want}`);
        }
      }
    }
    if (lineErrors.length) {
      fail('section line budget not met (2 / 2 / 3 / 1 / 1-2). Rewrite these fields in the data file:\n  - ' + lineErrors.join('\n  - '));
    }
    console.log('[export] Line budget OK on all ' + lineCounts.length + ' projects.');

    console.log('[export] Setting PDF metadata...');
    await page.evaluate((meta) => {
      document.title = meta.documentTitle;
    }, data.meta);

    console.log('[export] Printing PDF to ' + OUT_PATH);
    await page.pdf({
      path: OUT_PATH,
      format: 'Letter',
      printBackground: true,
      displayHeaderFooter: false,
      preferCSSPageSize: true,
      margin: { top: '0in', bottom: '0in', left: '0in', right: '0in' },
    });
  } finally {
    await browser.close();
  }

  const stats = fs.statSync(OUT_PATH);
  if (stats.size < 10 * 1024) {
    fail(`output PDF is suspiciously small (${stats.size} bytes) — export likely failed silently`);
  }

  console.log(`\n[export] Done. PDF written to:\n  ${OUT_PATH}\n  (${(stats.size / 1024).toFixed(1)} KB)\n`);
}

run().catch((err) => {
  fail(err && err.stack ? err.stack : String(err));
});
