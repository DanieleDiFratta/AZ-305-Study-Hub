"""Build a metadata-only inventory from public Microsoft pages (Python stdlib)."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
import re
from pathlib import Path
import time
import urllib.error
import urllib.request
from urllib.parse import urljoin, urlsplit, urlunsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from inspect_source import Page, ROOT

DATA = ROOT / 'data'
CACHE = ROOT / '.cache' / 'pages'
def rome_now():
    try:
        return datetime.now(ZoneInfo('Europe/Rome'))
    except ZoneInfoNotFoundError:
        # Windows may lack IANA tzdata. Current EU DST: last Sunday March/October, 01:00 UTC.
        now = datetime.now(timezone.utc)
        def boundary(month):
            end = datetime(now.year, month + 1, 1, tzinfo=timezone.utc) - timedelta(days=1)
            return end.replace(hour=1) - timedelta(days=(end.weekday() + 1) % 7)
        return now.astimezone(timezone(timedelta(hours=2 if boundary(3) <= now < boundary(10) else 1)))


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def normalize(url):
    s = urlsplit(url)
    return urlunsplit((s.scheme, s.netloc.lower(), s.path.rstrip('/'), '', ''))


def get_page(url, refresh=False):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / (sha256(url.encode()).hexdigest() + '.html')
    evidence = path.with_suffix('.json')
    if path.exists() and evidence.exists() and not refresh:
        return path.read_text(encoding='utf-8'), json.loads(evidence.read_text(encoding='utf-8'))
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'AZ305-Study-Hub metadata research/1.0'})
            with urllib.request.urlopen(req, timeout=40) as response:
                raw = response.read()
                meta = {'requested_url': url, 'resolved_url': response.url, 'http_status': response.status,
                        'checked_at': rome_now().isoformat(timespec='seconds'),
                        'content_type': response.headers.get('Content-Type', ''),
                        'response_sha256': sha256(raw).hexdigest(), 'method': 'GET'}
            html = raw.decode('utf-8', errors='replace')
            path.write_text(html, encoding='utf-8')
            evidence.write_text(json.dumps(meta, indent=2), encoding='utf-8')
            return html, meta
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            if attempt == 2:
                return '', {'requested_url': url, 'resolved_url': url,
                            'http_status': getattr(error, 'code', None),
                            'checked_at': rome_now().isoformat(timespec='seconds'),
                            'method': 'GET', 'error': str(error)}
            time.sleep(attempt + 1)


def inspect(seed, refresh=False):
    html, access = get_page(seed['url'], refresh)
    p = Page()
    p.feed(html)
    h1 = next((clean(h[2]) for h in p.headings if h[0] == 'h1'), '')
    # Read only article/main text for content evidence; avoid treating a sign-in banner as a gate.
    content = re.search(r'<main\b[^>]*>(.*?)</main>', html, re.S | re.I)
    body = Page()
    body.feed(content[1] if content else html)
    text = clean(' '.join(body.text))
    title = h1 or p.meta.get('og:title', seed.get('title_hint', ''))
    status = 'public_content' if access.get('http_status') == 200 and h1 and len(text) > 150 else 'unverified'
    if 'error' in access:
        status = 'unavailable' if access.get('http_status') in (404, 410) else 'check_failed'
    if re.search(r'\b404\b|\bpage not found\b|^sign in\b', h1.lower()):
        status = 'content_not_available'
    kind = seed['kind']
    notes = []
    if kind == 'learn_unit' and ('assessment' in title.lower() or 'knowledge check' in title.lower()):
        notes.append('Pagina pubblica; completamento/valutazione personale può richiedere login. Nessuna risposta raccolta.')
    if 'Access to this page requires authorization' in html and status == 'public_content':
        notes.append('Banner generico di autorizzazione nel template; corpo articolo leggibile tramite GET.')
    days = seed.get('recheck_days', 30 if kind in ('exam_guide', 'exam', 'lifecycle') else 60)
    result = {**seed, 'title': title, 'language': p.meta.get('locale', 'en-us'),
              'publisher': 'Microsoft', 'access': {**access, 'status': status, 'notes': notes},
              'verified_on': access['checked_at'][:10],
              'recheck_days': days,
              'next_review_on': (datetime.fromisoformat(access['checked_at']).date() + timedelta(days=days)).isoformat(),
              'source_updated_at': p.meta.get('updated_at'),
              'source_ms_date': p.meta.get('ms.date'),
              'source_commit_url': p.meta.get('gitcommit'),
              'source_uid': p.meta.get('uid'),
              'headings': [{'level': h[0], 'anchor': h[1], 'title': clean(h[2])} for h in p.headings if h[1]],
              'review_status': seed.get('review_status', 'metadata_checked'),
              'content_review': seed.get('content_review', '')}
    # Store link/structure evidence, without reproducing instructional bodies.
    result['outgoing_relevant_links'] = list(dict.fromkeys(
        urljoin(access['resolved_url'], u) for u, _ in p.links
        if urlsplit(urljoin(access['resolved_url'], u)).netloc == 'learn.microsoft.com'
        and any(x in urljoin(access['resolved_url'], u) for x in ('/training/modules/', '/training/paths/', '/azure/', '/entra/'))
    ))
    result['images'] = []
    for src, alt in re.findall(r'<img\b[^>]*src="([^"]+)"[^>]*alt="([^"]*)"', content[1] if content else '', re.I):
        if any(x in src.lower() for x in ('diagram', 'architecture', '/media/')):
            result['images'].append({'url': urljoin(access['resolved_url'], src), 'alt': alt,
                                     'access_status': 'embedded_reference_not_downloaded'})
    return result, p, html


def parallel(seeds, refresh=False):
    rows = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        pending = {pool.submit(inspect, seed, refresh): seed for seed in seeds}
        for future in as_completed(pending):
            row, p, html = future.result()
            rows.append((row, p, html))
            if row['access']['status'] != 'public_content':
                print(row['id'], row['access']['status'], row['access'].get('http_status'), flush=True)
    return sorted(rows, key=lambda x: x[0]['id'])


def write(name, data):
    DATA.mkdir(exist_ok=True)
    (DATA / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def extract_guide_structure(html, response_hash, groups):
    result = {}
    for g in groups:
        match = re.search(r'<h4\b[^>]*id="' + re.escape(g['source_anchor']) + r'"[^>]*>.*?</h4>\s*<ul>(.*?)</ul>', html, re.S)
        bullets = []
        if match:
            for li in re.findall(r'<li>(.*?)</li>', match[1], re.S):
                parser = Page()
                parser.feed(li)
                bullets.append(sha256(clean(' '.join(parser.text)).encode()).hexdigest())
        result[g['id']] = {'anchor':g['source_anchor'], 'count':len(bullets), 'bullet_sha256':bullets}
    return {'source_response_sha256':response_hash, 'groups':result}


def inventory(refresh=False):
    seeds = json.loads((DATA / 'seeds.json').read_text(encoding='utf-8'))
    base = parallel(seeds, refresh)
    rows = [r for r, _, _ in base]
    course, course_page, _ = next(item for item in base if item[0]['id'] == 'EXAM-COURSE')
    course['syllabus_path_uids'] = course_page.meta_all.get('learn_item', [])
    guide, _, guide_html = next(item for item in base if item[0]['id'] == 'EXAM-GUIDE')
    groups = json.loads((DATA / 'objectives.json').read_text(encoding='utf-8'))['groups']
    write('observed-guide.json', extract_guide_structure(guide_html, guide['access'].get('response_sha256'), groups))
    modules = {}
    for row, p, html in base:
        if row['kind'] != 'learn_path':
            continue
        found = {}
        for u, t in p.links:
            url = urljoin(row['access']['resolved_url'], u)
            if re.fullmatch(r'https://learn.microsoft.com/en-us/training/modules/[^/#?]+/', url):
                found.setdefault(url, clean(t))
        row['module_ids'] = []
        row['declared_module_count'] = int(re.search(r'(\d+) Modules', html)[1])
        for url, hint in found.items():
            slug = urlsplit(url).path.rstrip('/').split('/')[-1]
            mid = 'M-' + slug
            row['module_ids'].append(mid)
            if url not in modules:
                modules[url] = {'id': mid, 'url': url, 'kind': 'learn_module', 'path_ids': [],
                                'objective_ids': [], 'mapping_scope': 'module_context'}
            modules[url]['path_ids'].append(row['id'])
    module_rows = parallel(list(modules.values()), refresh)
    units = []
    for row, p, module_html in module_rows:
        row['unit_ids'] = []
        declared = re.search(r'(\d+) Units', module_html)
        row['declared_unit_count'] = int(declared[1]) if declared else None
        prefix = row['access']['resolved_url'].rstrip('/') + '/'
        found = {}
        for u, t in p.links:
            url = urljoin(row['access']['resolved_url'], u)
            if url.startswith(prefix) and re.fullmatch(r'[^/#?]+', url[len(prefix):]):
                found.setdefault(url, clean(t))
        for i, (url, hint) in enumerate(found.items(), 1):
            uid = row['id'].replace('M-', 'U-', 1) + '-' + str(i).zfill(2)
            row['unit_ids'].append(uid)
            units.append({'id': uid, 'url': url, 'kind': 'learn_unit', 'module_id': row['id'],
                          'unit_order': i, 'title_hint': hint, 'objective_ids': [],
                          'mapping_scope': 'pending_review'})
        rows.append(row)
    print(f'Discovered {len(modules)} unique modules and {len(units)} units', flush=True)
    write('resources.json', rows)
    write('unit-seeds.json', units)
    unit_rows = parallel(units, refresh)
    rows.extend(r for r, _, _ in unit_rows)
    write('resources.json', sorted(rows, key=lambda r: r['id']))
    print(f'Saved {len(rows)} resources', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--refresh', action='store_true')
    args = parser.parse_args()
    inventory(args.refresh)
