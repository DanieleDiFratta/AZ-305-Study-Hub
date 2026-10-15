"""Build the public dashboard with Python's standard library; never rewrite study data."""
from datetime import date
from html import escape
import json
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET

from catalogue import assemble, load
from research import rome_now

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '_site'
STATES = ('proposed', 'read', 'discussed', 'practiced', 'verified')
BLOCK_IDS = ['LP-PREREQ', 'LP-IDENTITY', 'LP-BCDR', 'LP-DATA', 'LP-INFRA', 'LP-WAF']
# Exam objectives remain visible even where Learn has no dedicated unit.
PATH_DOMAINS = {'LP-IDENTITY': '1', 'LP-DATA': '2', 'LP-BCDR': '3', 'LP-INFRA': '4'}


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def plain(text):
    return text.replace('`', '').replace('**', '')


def curriculum(objectives, resources):
    """Follow the course syllabus, then each path's modules and units in source order."""
    paths = {r['source_uid']: r for r in resources.values() if r['kind'] == 'learn_path'}
    ordered = [paths[uid] for uid in resources['EXAM-COURSE']['syllabus_path_uids']]
    if [p['id'] for p in ordered] != BLOCK_IDS:
        raise ValueError('Ordine dei learning path diverso dal syllabus accettato: esaminare la modifica')
    blocks = []
    for i, path in enumerate(ordered):
        bid = path['id']
        modules = [{'id': mid, 'unit_ids': resources[mid]['unit_ids']} for mid in path['module_ids']]
        source_ids = [bid] + [rid for m in modules for rid in [m['id'], *m['unit_ids']]]
        mapped = {oid for rid in source_ids for oid in resources[rid]['objective_ids']}
        objective_ids = [o['id'] for o in objectives if o['id'] in mapped or o['domain'] == PATH_DOMAINS.get(bid)]
        blocks.append({'id': bid, 'title': path['title'], 'objective_ids': objective_ids,
                       'prerequisites': [ordered[i - 1]['id']] if i else [],
                       'theory': 'Seguire i moduli e le unità Microsoft Learn nell’ordine riportato. Le letture aggiuntive saranno proposte per dubbi, aggiornamenti o lacune specifiche.',
                       'practice': 'Lettura autonoma, dubbi, spiegazione quando sei pronto e verifica integrata. Gli assessment restano nel punto previsto dal modulo; eventuali laboratori saranno definiti prima di eseguirli.',
                       'outcome': 'Discutere e verificare i contenuti effettivamente studiati, conservando separati lettura, discussione, esercizio e comprensione.',
                       'estimate': f'{len(modules)} moduli · tempo da calibrare',
                       'resource_ids': source_ids, 'modules': modules})
    return blocks


def validate_progress(progress, objectives):
    if progress.get('schema_version') != 1:
        raise ValueError('Versione progressi non supportata')
    date.fromisoformat(progress['updated_on'])
    date.fromisoformat(progress['exam_date'])
    if progress['resume']['block_id'] not in BLOCK_IDS:
        raise ValueError('Punto di ripresa: blocco inesistente')
    for collection, allowed in [('objectives', {o['id'] for o in objectives}), ('blocks', set(BLOCK_IDS))]:
        for oid, flags in progress[collection].items():
            if oid not in allowed:
                raise ValueError('Progresso con ID inesistente: ' + oid)
            for state, evidence in flags.items():
                if state not in STATES or not isinstance(evidence, dict):
                    raise ValueError('Stato non valido: ' + state)
                date.fromisoformat(evidence['on'])
                if not evidence.get('evidence', '').strip():
                    raise ValueError('Ogni progresso richiede evidenza: ' + oid)
    for session in progress['sessions']:
        date.fromisoformat(session['date'])
        if session['block_id'] not in BLOCK_IDS or not session['summary'].strip():
            raise ValueError('Sessione non valida')
    for doubt in progress['doubts']:
        if doubt['block_id'] not in BLOCK_IDS or not doubt['text'].strip():
            raise ValueError('Dubbio non valido')
        if doubt.get('resolved_on'):
            date.fromisoformat(doubt['resolved_on'])
    for review in progress['reviews']:
        date.fromisoformat(review['due_on'])
        if review['block_id'] not in BLOCK_IDS or not review['reason'].strip():
            raise ValueError('Richiamo non valido')
        if review.get('completed_on'):
            date.fromisoformat(review['completed_on'])


def safe_url(url):
    return url.startswith(('https://', 'http://', '#'))


def inline(text):
    """Escape HTML first; support a deliberately small, safe Markdown subset."""
    value = escape(text)
    def link(match):
        label, url = match.groups()
        if not safe_url(url):
            return label
        attrs = '' if url.startswith('#') else ' target="_blank" rel="noopener noreferrer"'
        return f'<a href="{url}"{attrs}>{label}</a>'
    value = re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)', link, value)
    value = re.sub(r'`([^`]+)`', r'<code>\1</code>', value)
    value = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', value)
    return value


def markdown(text):
    result, list_tag, in_code = [], None, False
    for line in text.splitlines():
        if line.startswith('```'):
            if list_tag:
                result.append(f'</{list_tag}>'); list_tag = None
            result.append('</code></pre>' if in_code else '<pre><code>')
            in_code = not in_code
            continue
        if in_code:
            result.append(escape(line) + '\n'); continue
        item = re.match(r'^\s*(?:[-*]|\d+\.)\s+(.+)', line)
        desired = ('ol' if re.match(r'^\s*\d+\.', line) else 'ul') if item else None
        if list_tag and list_tag != desired:
            result.append(f'</{list_tag}>'); list_tag = None
        if desired and list_tag != desired:
            result.append(f'<{desired}>'); list_tag = desired
        if item:
            result.append('<li>' + inline(item[1]) + '</li>')
        elif heading := re.match(r'^(#{1,6})\s+(.+)', line):
            level = min(6, len(heading[1]) + 1)
            result.append(f'<h{level}>' + inline(heading[2]) + f'</h{level}>')
        elif line.strip():
            result.append('<p>' + inline(line) + '</p>')
    if list_tag: result.append(f'</{list_tag}>')
    if in_code: result.append('</code></pre>')
    return '\n'.join(result)


def materials(manifest):
    if manifest.get('schema_version') != 1:
        raise ValueError('Versione materiali non supportata')
    items, ids = [], set()
    for entry in manifest['items']:
        item = dict(entry)
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', item['id']) or item['id'] in ids:
            raise ValueError('ID materiale non valido o duplicato')
        ids.add(item['id'])
        if not item.get('title', '').strip():
            raise ValueError('Titolo del materiale mancante')
        if item['kind'] not in ('notes', 'map', 'flashcards') or item['block_id'] not in BLOCK_IDS:
            raise ValueError('Tipo o blocco materiale non valido')
        date.fromisoformat(item['published_on'])
        relative = Path(item.pop('path'))
        path = (ROOT / relative).resolve()
        if relative.is_absolute() or not path.is_relative_to((ROOT / 'studio/ripasso').resolve()) or path.is_symlink():
            raise ValueError('I materiali devono risiedere in studio/ripasso')
        if item['kind'] == 'flashcards':
            cards = read_json(path)
            if not isinstance(cards, list) or not cards or any(not isinstance(c, dict) or not isinstance(c.get('question'), str) or not c['question'].strip() or not isinstance(c.get('answer'), str) or not c['answer'].strip() for c in cards):
                raise ValueError('Flashcard prive di domanda o risposta')
            item['cards'] = cards
        elif item['kind'] == 'map' and path.suffix == '.svg':
            svg = path.read_text(encoding='utf-8')
            allowed = {'svg', 'g', 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path', 'text', 'tspan', 'title', 'desc', 'defs', 'marker'}
            root = ET.fromstring(svg)
            if root.tag.split('}')[-1] != 'svg' or not root.get('viewBox'):
                raise ValueError('La mappa SVG richiede viewBox')
            for element in root.iter():
                if element.tag.split('}')[-1] not in allowed:
                    raise ValueError('Elemento SVG non consentito')
                for attr, value in element.attrib.items():
                    if attr.split('}')[-1].lower().startswith('on') or attr.split('}')[-1].lower() in ('href', 'style') or re.search(r'url\((?!#[a-zA-Z0-9_-]+\))', value, re.I):
                        raise ValueError('Attributo SVG non consentito')
            item['html'] = f'<figure class="study-map">{svg}<figcaption>{escape(item.get("summary", item["title"]))}</figcaption></figure>'
        else:
            if path.suffix != '.md':
                raise ValueError('Usare Markdown per gli appunti, Markdown o SVG per le mappe')
            item['html'] = markdown(path.read_text(encoding='utf-8'))
        items.append(item)
    return items


def build(output=OUTPUT):
    baseline = load('objectives.json')
    rows = assemble()
    byid = {r['id']: r for r in rows}
    progress = read_json(ROOT / 'studio/progressi.json')
    validate_progress(progress, baseline['objectives'])
    if progress['resume'].get('source_id') and progress['resume']['source_id'] not in byid:
        raise ValueError('Fonte del punto di ripresa inesistente')
    resources = []
    for r in rows:
        resources.append({**{key: r.get(key) for key in ['id', 'title', 'url', 'kind', 'objective_ids', 'mapping_scope', 'verified_on', 'next_review_on', 'language', 'selection_reason_it', 'review_current']},
                          'status': r['access']['status'], 'http_status': r['access'].get('http_status'),
                          'role': r['review']['coverage_role'], 'flags': r['review'].get('flags', [])})
    payload = {'built_on': rome_now().date().isoformat(), 'baseline': baseline,
               'blocks': curriculum(baseline['objectives'], byid), 'resources': resources,
               'progress': progress, 'materials': materials(read_json(ROOT / 'studio/materiali.json'))}
    output.mkdir(parents=True, exist_ok=True)
    for name in ['index.html', 'style.css', 'app.js', 'favicon.svg']:
        shutil.copyfile(ROOT / 'web' / name, output / name)
    # A JS data file also permits a local preview by opening index.html directly.
    serialized = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    (output / 'site-data.js').write_text('window.STUDY_DATA=' + serialized + ';\n', encoding='utf-8')
    (output / '.nojekyll').write_text('', encoding='utf-8')
    print(f'Dashboard: {len(payload["blocks"])} blocchi, {len(resources)} fonti, {len(payload["materials"])} materiali → {output}')
    return payload


if __name__ == '__main__':
    build()
