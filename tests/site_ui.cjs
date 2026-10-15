/* Optional DOM checks. jsdom is a QA tool in .cache, never a site dependency. */
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM } = require('../.cache/site-qa/node_modules/jsdom');
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'web/index.html'), 'utf8');
const app = fs.readFileSync(path.join(root, 'web/app.js'), 'utf8');
const dataset = fs.readFileSync(path.join(root, '_site/site-data.js'), 'utf8');

function open(hash = '#home', change = () => {}, now = '2026-10-15T18:00:00Z') {
  const dom = new JSDOM(html, { url: 'https://example.com/AZ-305-Study-Hub/' + hash, runScripts: 'outside-only' });
  const { window } = dom;
  const RealDate = window.Date;
  window.Date = class extends RealDate { constructor(...args) { super(...(args.length ? args : [now])); } static now() { return new RealDate(now).valueOf(); } };
  window.scrollTo = () => {};
  window.HTMLElement.prototype.scrollIntoView = () => {};
  window.eval(dataset);
  change(window.STUDY_DATA);
  const originalProgress = JSON.stringify(window.STUDY_DATA.progress);
  window.eval(app);
  return { dom, window, document: window.document, originalProgress };
}

function input(window, selector, value, event = 'input') {
  const node = window.document.querySelector(selector);
  node.value = value;
  node.dispatchEvent(new window.Event(event, { bubbles: true }));
}

test('Home separates valid source coverage from zero personal progress', () => {
  const { dom, document } = open();
  assert.equal(document.querySelector('h1').textContent, 'Il tuo prossimo passo.');
  const values = [...document.querySelectorAll('.stat-value')].map(n => n.textContent.trim());
  assert.deepEqual(values, ['47', '0 / 49', '0', '0']);
  assert.match(document.querySelector('.callout').textContent, /49\/49/);
  assert.equal(document.querySelectorAll('.domain').length, 4);
  assert.equal(document.querySelectorAll('progress[value="0"]').length, 4);
  dom.window.close();
});

test('All 12 blocks and the on-premises Learn gap are visible', () => {
  const pathPage = open('#percorso');
  assert.equal(pathPage.document.querySelectorAll('.block-card').length, 12);
  assert.equal(pathPage.document.querySelector('.block-card.current').getAttribute('href'), '#blocco/S00');
  pathPage.dom.window.close();
  const block = open('#blocco/S02');
  assert.equal(block.document.querySelectorAll('.objectives>li').length, 9);
  assert.match(block.document.querySelector('.objectives').textContent, /1\.2\.4/);
  assert.match(block.document.querySelector('.objectives').textContent, /Nessuna unità Learn dedicata/);
  assert.equal(block.document.querySelectorAll('.state.done').length, 0);
  block.dom.window.close();
});

test('Library search and filters work without losing input focus or writing progress', () => {
  const { dom, window, document, originalProgress } = open('#biblioteca');
  assert.equal(document.querySelectorAll('.library-grid .resource').length, 20);
  assert.match(document.querySelector('#library-summary').textContent, /378 risorse/);
  document.querySelector('#resource-search').focus();
  input(window, '#resource-search', '1.2.4');
  input(window, '#kind-filter', 'documentation', 'change');
  assert.match(document.querySelector('#library-summary').textContent, /2 risorse/);
  assert.match(document.querySelector('#library-results').textContent, /ID-ONPREM/);
  assert.equal(document.activeElement.id, 'resource-search');
  assert.equal(JSON.stringify(window.STUDY_DATA.progress), originalProgress);
  assert.equal(window.localStorage.length, 0);
  assert.equal(window.sessionStorage.length, 0);
  dom.window.close();
});

test('Placeholder filter exposes exactly the unavailable case entries', () => {
  const { dom, window, document } = open('#biblioteca');
  input(window, '#kind-filter', 'placeholder', 'change');
  assert.match(document.querySelector('#library-summary').textContent, /3 risorse/);
  assert.equal(document.querySelectorAll('.resource .tag.orange').length, 3);
  assert.equal(document.querySelectorAll('.resource .tag.green').length, 0);
  dom.window.close();
});

test('Library pagination and bookmarked filters work under the repository subpath', () => {
  const { dom, window, document } = open('#biblioteca');
  const first = document.querySelector('.resource a').textContent;
  document.querySelector('#next-page').click();
  assert.match(window.location.hash, /page=2/);
  assert.notEqual(document.querySelector('.resource a').textContent, first);
  document.querySelector('#previous-page').click();
  assert.equal(document.querySelector('.resource a').textContent, first);
  input(window, '#resource-search', 'dns');
  input(window, '#domain-filter', '4', 'change');
  const bookmark = window.location.hash;
  const reload = open(bookmark);
  assert.equal(reload.document.querySelector('#resource-search').value, 'dns');
  assert.equal(reload.document.querySelector('#domain-filter').value, '4');
  assert.equal(reload.document.querySelector('#library-summary').textContent, document.querySelector('#library-summary').textContent);
  dom.window.close(); reload.dom.window.close();
});

test('Search text and unsupported routes cannot inject HTML', () => {
  const { dom, window, document } = open('#biblioteca?q=%3Cimg%20src=x%20onerror=alert(1)%3E');
  assert.equal(document.querySelectorAll('img').length, 0);
  assert.match(document.querySelector('#library-summary').textContent, /0 risorse/);
  input(window, '#resource-search', '<script>bad</script>');
  assert.equal(document.querySelectorAll('#main script').length, 0);
  const missing = open('#blocco/inesistente');
  assert.match(missing.document.querySelector('h1').textContent, /pagina non c’è/);
  const malformed = open('#%ZZ');
  assert.match(malformed.document.querySelector('h1').textContent, /pagina non c’è/);
  dom.window.close(); missing.dom.window.close(); malformed.dom.window.close();
});

test('Future source expiration never erases personal verification', () => {
  const { dom, document } = open('#home', data => {
    data.progress.objectives['1.1.1'] = { verified: { on: '2026-10-15', evidence: 'Fixture di test' } };
  }, '2027-01-14T12:00:00Z');
  assert.match(document.querySelector('.callout').textContent, /0\/49/);
  assert.match(document.querySelectorAll('.stat-value')[1].textContent, /1 \/ 49/);
  dom.window.close();
});

test('Review collections filter real published material and have an honest empty state', () => {
  const emptyPage = open('#ripasso?kind=map');
  assert.match(emptyPage.document.querySelector('.empty').textContent, /Non ci sono ancora materiali/);
  emptyPage.dom.window.close();
  const { dom, document } = open('#ripasso', data => {
    data.materials = [
      { id: 'test-note', kind: 'notes', block_id: 'S01', title: 'Appunti di test', published_on: '2026-10-15', html: '<p>Fixture</p>' },
      { id: 'test-map', kind: 'map', block_id: 'S02', title: 'Mappa di test', published_on: '2026-10-15', html: '<p>Fixture</p>' }
    ];
  });
  assert.equal(document.querySelectorAll('.material-card').length, 2);
  document.querySelector('[data-kind="map"]').click();
  assert.equal(document.querySelectorAll('.material-card').length, 1);
  assert.match(document.querySelector('.material-card').textContent, /Mappa di test/);
  dom.window.close();
});

test('Flashcards reveal answers on demand, reset on navigation, and record no progress', () => {
  const { dom, window, document, originalProgress } = open('#materiale/carte-test', data => {
    data.materials = [{ id: 'carte-test', kind: 'flashcards', block_id: 'S00', title: 'Fixture di test', published_on: '2026-10-15', cards: [{ question: 'Prima domanda', answer: 'Prima risposta' }, { question: 'Seconda domanda', answer: 'Seconda risposta' }] }];
  });
  assert.equal(document.querySelector('#card-answer').hidden, true);
  document.querySelector('#reveal-answer').click();
  assert.equal(document.querySelector('#card-answer').hidden, false);
  assert.equal(document.querySelector('#reveal-answer').getAttribute('aria-expanded'), 'true');
  document.querySelector('#card-next').click();
  assert.equal(document.querySelector('#card-question').textContent, 'Seconda domanda');
  assert.equal(document.querySelector('#card-answer').hidden, true);
  assert.equal(document.querySelector('#card-next').disabled, true);
  assert.equal(JSON.stringify(window.STUDY_DATA.progress), originalProgress);
  dom.window.close();
});

test('Skip link moves focus to content without changing the active route', () => {
  const { dom, window, document } = open('#home');
  document.querySelector('.skip-link').click();
  assert.equal(document.activeElement.id, 'main');
  assert.equal(window.location.hash, '#home');
  dom.window.close();
});
