"""Discover case-study pages and diagram URLs from already fetched official indexes."""
from concurrent.futures import ThreadPoolExecutor
import argparse
from datetime import timedelta
from hashlib import sha256
import json
import re
import urllib.request
from urllib.parse import urljoin

from inspect_source import Page, ROOT
from research import get_page, parallel, rome_now, write

rows = json.loads((ROOT / 'data/resources.json').read_text(encoding='utf-8'))
parser = argparse.ArgumentParser()
parser.add_argument('--refresh', action='store_true')
args = parser.parse_args()
index = next(r for r in rows if r['id'] == 'LAB-INDEX')
html, _ = get_page(index['url'])
p = Page()
p.feed(html)
cases = []
seen = set()
for u, title in p.links:
    url = urljoin(index['url'], u)
    match = re.search(r'/Instructions/CaseStudy/(\d+)-.*\.html$', url)
    if not match or not title.strip() or url in seen:
        continue
    seen.add(url)
    cases.append({'id': 'LAB-' + match[1], 'url': url, 'title_hint': title.strip(),
                  'kind': 'official_case', 'parent_id': 'LAB-INDEX', 'objective_ids': [],
                  'selection_reason_it': 'Caso MicrosoftLearning individuato nell’indice ufficiale; nessuna soluzione copiata.',
                  'mapping_scope': 'support', 'review_status': 'pending_content_review'})
case_rows = [r for r, _, _ in parallel(cases, args.refresh)]
for r in case_rows:
    if r['id'] in ('LAB-05', 'LAB-10', 'LAB-11'):
        # These index entries explicitly state that no formal case study is supplied.
        r['exercise_status'] = 'no_formal_case_study'
    elif r['id'] == 'LAB-12':
        r['exercise_status'] = 'optional_outside_explicit_exam_bullets'
    else:
        r['exercise_status'] = 'case_available_not_performed'

diagrams = []
for r in rows:
    if r['kind'] != 'reference_architecture':
        continue
    for n, img in enumerate(r['images'][:2 if r['id'] in ('ARC-DATA', 'ARC-DR') else 1], 1):
        diagrams.append({'id': 'FIG-' + r['id'][4:] + '-' + str(n), 'url': img['url'],
                         'title': f"Diagramma {n}: {r['title']}", 'kind': 'diagram',
                         'parent_id': r['id'], 'objective_ids': r['objective_ids'],
                         'language': 'en-us', 'publisher': 'Microsoft', 'mapping_scope': 'support',
                         'selection_reason_it': 'Diagramma collegato dalla pagina architetturale; leggere il contesto prima di riutilizzarlo.',
                         'recheck_days': 60})

def verify_diagram(seed):
    r = dict(seed)
    request = urllib.request.Request(r['url'], headers={'User-Agent': 'AZ305-Study-Hub metadata research/1.0'})
    try:
        with urllib.request.urlopen(request, timeout=35) as response:
            data = response.read()
            mime = response.headers.get('Content-Type', '')
            r['access'] = {'method': 'GET', 'requested_url': r['url'], 'resolved_url': response.url,
                           'http_status': response.status, 'content_type': mime,
                           'checked_at': rome_now().isoformat(timespec='seconds'),
                           'response_sha256': sha256(data).hexdigest(),
                           'status': 'public_asset' if response.status == 200 and ('image/' in mime or 'svg' in mime) else 'unverified',
                           'notes': ['Verificati risposta, MIME e hash; file originale non distribuito nel repository.']}
    except Exception as error:
        r['access'] = {'method': 'GET', 'http_status': getattr(error, 'code', None),
                       'status': 'check_failed', 'error': str(error),
                       'checked_at': rome_now().isoformat(timespec='seconds')}
    r['verified_on'] = r['access']['checked_at'][:10]
    r['next_review_on'] = (rome_now().date() + timedelta(days=r['recheck_days'])).isoformat()
    return r

with ThreadPoolExecutor(max_workers=6) as pool:
    extra = case_rows + list(pool.map(verify_diagram, diagrams))
write('extra-resources.json', extra)
print(f'Verified {len(case_rows)} case entries and {len(diagrams)} diagram assets')
for r in extra:
    print(r['id'], r['access']['status'], r['title'])
