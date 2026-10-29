/*
 * Jobsite Intelligence report renderer (adapted from Austin Signage Intelligence's template).
 * Exposes window.renderReport(data) which populates #report-root with a
 * short, scannable report built from report-data.json:
 *   page 1 — cover + at-a-glance table
 *   pages 2..N — projects, two per page (last page may hold one)
 *   final page — pilot offer
 * Used both by index.html (via fetch, for local preview through a static
 * server) and by the Playwright export script (which injects the parsed
 * JSON directly, sidestepping file:// fetch restrictions).
 */
(function () {
  function esc(str) {
    if (str === undefined || str === null) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function eyebrowMark(color) {
    return '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M13 33 L13 15 L31 15" fill="none" stroke="' + color + '" stroke-width="8" stroke-linecap="square"/></svg>';
  }

  function logoLockup() {
    return (
      '<div class="logo-mark">' +
      '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M13 33 L13 15 L31 15" fill="none" stroke="#101010" stroke-width="7" stroke-linecap="square"/><path d="M51 31 L51 49 L33 49" fill="none" stroke="#101010" stroke-width="7" stroke-linecap="square"/></svg>' +
      '<span>Asterfield</span>' +
      '</div>'
    );
  }

  // The sender name shown in the running header strip on every page is
  // derived from report.city so no market name is ever hardcoded here —
  // report-data*.json is the only place a city name needs to be set.
  function senderName(data) {
    return esc((data.report.city || '').toUpperCase()) + ' JOBSITE INTELLIGENCE';
  }

  function docHeader(data, pageNum) {
    return (
      '<div class="doc-header">' +
      logoLockup() +
      '<span>' + senderName(data) + ' / ' + esc(data.report.reportShortLabel) + ' / ' + pageNum + '</span>' +
      '</div>'
    );
  }

  function docFooter(data) {
    return (
      '<div class="doc-footer">' +
      '<span>' + esc(data.report.footerLine) + '</span>' +
      '<span>' + esc(data.brand.companyLine) + '</span>' +
      '</div>'
    );
  }

  function tagClass(tag) {
    return /^portable/i.test(tag) ? 'tag-install' : 'tag-full';
  }

  // TDLR TABS records carry a real, state-filed construction start date.
  // City-permit records (recordLabel like "Austin permit ...") only carry
  // the date the permit was issued, a different fact — the city has no
  // equivalent "start date" field. Label each project's date field to
  // match what it actually is, driven off the record source, so this
  // never has to be set by hand per project.
  function filedLabel(p) {
    if (p.dateLabel) return p.dateLabel;
    if (/^TCEQ/i.test(p.recordLabel)) return 'Authorized';
    return /^TDLR/i.test(p.recordLabel) ? 'Filed start' : 'Permit issued';
  }

  function renderCover(data) {
    var r = data.report;
    var rows = data.projects.map(function (p) {
      return (
        '<div class="glance-row">' +
        '<div class="g-num">' + esc(p.number) + '</div>' +
        '<div class="g-name">' + esc(p.name) + '<span class="g-addr">' + esc(p.area) + '</span></div>' +
        '<div class="g-tag"><span class="tag-pill ' + tagClass(p.tag) + '">' + esc(p.tag) + '</span></div>' +
        '<div class="g-filed"><span class="g-filed-label">' + esc(filedLabel(p)) + '</span>' + esc(p.filedStart) + '</div>' +
        '<div class="g-value">' + esc(p.value) + '</div>' +
        '<div class="g-record">' + esc(p.recordLabel) + '</div>' +
        '</div>'
      );
    }).join('');

    return (
      '<section class="page">' +
      '<div class="page-pad">' +
      docHeader(data, '01') +
      '<div class="cover-body">' +
      '<div class="eyebrow">' + eyebrowMark('#6E6E6B') + esc(r.eyebrow) + '</div>' +
      '<h1>' + esc(r.headline) + '</h1>' +
      '<p class="lede">' + esc(r.supportingCopy) + '</p>' +
      '<div class="cover-stats">' +
      '<div class="stat"><b>' + esc(r.territory) + '</b><span>Territory</span></div>' +
      '<div class="stat"><b>' + esc(r.projectCountLabel) + '</b><span>Included</span></div>' +
      '<div class="stat"><b>' + esc(r.preparedDate.replace(/^Prepared\s+/, '')) + '</b><span>Prepared</span></div>' +
      '</div>' +
      '</div>' +
      '<div class="glance-block">' +
      '<div class="glance-head">' +
      '<div class="g-num">#</div>' +
      '<div class="g-name">Project</div>' +
      '<div class="g-tag">Type</div>' +
      '<div class="g-filed">Timing</div>' +
      '<div class="g-value">' + esc((data.projects[0] && data.projects[0].valueLabel) || 'From yard') + '</div>' +
      '<div class="g-record">Record</div>' +
      '</div>' +
      rows +
      '</div>' +
      docFooter(data) +
      '</div>' +
      '</section>'
    );
  }

  function renderProjectCard(p, scopeLabel) {
    return (
      '<div class="proj-card avoid-break" data-project="' + esc(p.number) + ' ' + esc(p.name) + '">' +
      '<div class="proj-head">' +
      '<div class="proj-title"><span class="proj-num">' + esc(p.number) + '</span><h2>' + esc(p.name) + '</h2></div>' +
      '<span class="tag-pill ' + tagClass(p.tag) + '">' + esc(p.tag) + '</span>' +
      '</div>' +
      '<p class="proj-address">' + esc(p.address) + '</p>' +

      '<div class="proj-facts">' +
      '<div><div class="fact-label">' + esc(filedLabel(p)) + '</div><div class="fact-value">' + esc(p.filedStart) + '</div></div>' +
      '<div><div class="fact-label">' + esc(p.valueLabel || 'From your yard') + '</div><div class="fact-value">' + esc(p.value) + '</div></div>' +
      '<div><div class="fact-label">Record</div><div class="fact-value">' +
      '<a href="' + esc(p.recordUrl) + '">' + esc(p.recordLabel) + '</a></div></div>' +
      '</div>' +

      '<div class="proj-lines">' +
      '<div class="pl-row"><span class="pl-label">What&rsquo;s filed</span><span class="pl-value" data-field="whatsFiled">' + esc(p.whatsFiled) + '</span></div>' +
      '<div class="pl-row"><span class="pl-label">' + esc(scopeLabel) + '</span><span class="pl-value" data-field="likelyScope">' + esc(p.likelyScope) + '</span></div>' +
      '<div class="pl-row"><span class="pl-label">Who decides / what&rsquo;s unknown</span><span class="pl-value" data-field="whoDecides">' + esc(p.whoDecides) + '</span></div>' +
      '<div class="pl-row"><span class="pl-label">Contact</span><span class="pl-value" data-field="contactLine">' + esc(p.contactLine) + '</span></div>' +
      '<div class="pl-row"><span class="pl-label">Suggested first step</span><span class="pl-value" data-field="firstStep">' + esc(p.firstStep) + '</span></div>' +
      '</div>' +
      '</div>'
    );
  }

  function renderProjectPages(data, pageNumStart) {
    var pages = [];
    var projects = data.projects;
    var scopeLabel = data.report.scopeLabel || 'Likely hauling work (our read)';
    for (var i = 0; i < projects.length; i += 2) {
      var chunk = projects.slice(i, i + 2);
      var cards = chunk.map(function (p) { return renderProjectCard(p, scopeLabel); }).join('<hr class="proj-divider">');
      var pageNum = String(pageNumStart + pages.length).padStart(2, '0');
      pages.push(
        '<section class="page">' +
        '<div class="page-pad">' +
        docHeader(data, pageNum) +
        '<div class="proj-page-body">' + cards + '</div>' +
        docFooter(data) +
        '</div>' +
        '</section>'
      );
    }
    return pages.join('');
  }

  function renderPilot(data, pageNum) {
    var p = data.pilot;
    var items = p.bullets.map(function (b) {
      return '<div class="item"><span class="mark">&bull;</span><span>' + esc(b) + '</span></div>';
    }).join('');
    return (
      '<section class="page pilot-page">' +
      '<div class="page-pad">' +
      docHeader(data, pageNum) +
      '<div class="pilot-body">' +
      '<div class="eyebrow">' + eyebrowMark('#6E6E6B') + esc(p.eyebrow) + '</div>' +
      '<h1>' + esc(p.headline) + '</h1>' +
      '<div class="pilot-deliverables">' + items + '</div>' +
      (p.disclosure ? '<p class="pilot-disclosure">' + esc(p.disclosure) + '</p>' : '') +
      '<div class="cta-primary">' + esc(p.contactLine) + '</div>' +
      '</div>' +
      docFooter(data) +
      '</div>' +
      '</section>'
    );
  }

  function renderReport(data) {
    var root = document.getElementById('report-root');
    if (!root) throw new Error('render-report.js: #report-root not found in DOM');

    if (document.title !== undefined) {
      document.title = data.meta.documentTitle;
    }

    var projectPageCount = Math.ceil(data.projects.length / 2);
    var pilotPageNum = String(2 + projectPageCount).padStart(2, '0');

    var html = '';
    html += renderCover(data);
    html += renderProjectPages(data, 2);
    html += renderPilot(data, pilotPageNum);

    root.innerHTML = html;
    root.setAttribute('data-render-complete', 'true');
  }

  window.renderReport = renderReport;
})();
