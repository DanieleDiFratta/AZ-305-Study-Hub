"""Offline integrity, freshness, source drift and coverage checks. Exit nonzero on gaps."""
from collections import Counter
from datetime import date
import json
import re
import sys
from urllib.parse import unquote, urlsplit

from inspect_source import ROOT
from research import normalize, rome_now
from catalogue import assemble, coverage, load


def validate_data(rows, baseline, observed, accepted, today=None):
    today = today or rome_now().date()
    errors = []
    objectives = baseline['objectives']
    oids = {o['id'] for o in objectives}
    byid = {r['id']:r for r in rows}
    if len(byid) != len(rows):
        errors.append('ID risorsa duplicati')
    if len(oids) != len(objectives):
        errors.append('ID obiettivo duplicati')
    expected_ids = {f"{g['id']}.{i}" for g in baseline['groups'] for i in range(1, g['expected_bullets']+1)}
    if oids != expected_ids:
        errors.append('Elenco obiettivi incompleto rispetto ai gruppi/bullet della baseline')
    if observed.get('groups') != accepted.get('groups'):
        errors.append('La struttura o il testo dei bullet ufficiali è cambiato dopo la revisione')
    for g in baseline['groups']:
        if observed.get('groups', {}).get(g['id'], {}).get('count') != g['expected_bullets']:
            errors.append('Conteggio bullet non corrispondente: '+g['id'])
    finals = Counter()
    for r in rows:
        rid = r['id']
        url = urlsplit(r['url'])
        official = (url.netloc in ('learn.microsoft.com','www.microsoft.com') or
                    url.netloc == 'microsoftlearning.github.io' or
                    (url.netloc == 'github.com' and url.path.startswith('/MicrosoftLearning/')))
        if url.scheme != 'https' or not official:
            errors.append(rid+': origine non inclusa nel perimetro ufficiale')
        if not r['title'].strip() or not r.get('language'):
            errors.append(rid+': titolo o lingua mancanti')
        if set(r['objective_ids']) - oids:
            errors.append(rid+': obiettivo inesistente')
        if r['access'].get('http_status') != 200:
            errors.append(rid+': HTTP non verificato/200')
        if r['access']['status'] not in ('public_content','public_asset','public_placeholder'):
            errors.append(rid+': contenuto non verificato')
        if date.fromisoformat(r['verified_on']) > today:
            errors.append(rid+': verifica datata nel futuro')
        if date.fromisoformat(r['next_review_on']) < today:
            errors.append(rid+': verifica scaduta')
        current = bool(r.get('review') and r['review'].get('reviewed_response_sha256') and
                       r['review']['reviewed_response_sha256'] == r['access'].get('response_sha256'))
        if not current or not r['review_current']:
            errors.append(rid+': risposta cambiata o revisione mancante')
        if r['mapping_scope'] in ('module_context','path_context','reference','placeholder') and r['review']['coverage_role'] == 'primary':
            errors.append(rid+': contesto/placeholder promosso impropriamente a fonte primaria')
        finals[normalize(r['access'].get('resolved_url',r['url']))] += 1
        if r['kind'] == 'learn_path':
            if len(r['module_ids']) != r['declared_module_count']:
                errors.append(rid+': numero moduli diverso da quello dichiarato')
            for mid in r['module_ids']:
                if mid not in byid or rid not in byid[mid].get('path_ids',[]):
                    errors.append(rid+': appartenenza modulo incoerente: '+mid)
        if r['kind'] == 'learn_module':
            if len(r['unit_ids']) != r.get('declared_unit_count'):
                errors.append(rid+': numero unità diverso da quello dichiarato')
            for i, uid in enumerate(r['unit_ids'], 1):
                if uid not in byid or byid[uid].get('module_id') != rid or byid[uid].get('unit_order') != i:
                    errors.append(rid+': unità/ordine incoerente: '+uid)
        if r['kind'] == 'learn_unit':
            if r['module_id'] not in byid or rid not in byid[r['module_id']].get('unit_ids',[]):
                errors.append(rid+': unità orfana')
        if r['kind'] in ('diagram','official_case') and r['parent_id'] not in byid:
            errors.append(rid+': genitore mancante')
    if any(n > 1 for n in finals.values()):
        errors.append('URL finali normalizzati duplicati')
    course = byid.get('EXAM-COURSE',{})
    path_uids = {r['source_uid'] for r in rows if r['kind']=='learn_path'}
    if set(course.get('syllabus_path_uids',[])) != path_uids:
        errors.append('I percorsi non corrispondono a tutti i learn_item del corso ufficiale')
    if byid.get('EXAM-GUIDE',{}).get('access',{}).get('response_sha256') != observed.get('source_response_sha256'):
        errors.append('La prova della struttura non corrisponde alla risposta della guida')
    matrix = coverage(rows,objectives)
    for o in matrix:
        # Re-evaluate primary source evidence, instead of trusting a cached percentage.
        valid = [byid[rid] for rid in o['primary_resource_ids'] if byid[rid]['access']['status']=='public_content'
                 and byid[rid]['access'].get('http_status')==200 and byid[rid]['review_current']
                 and date.fromisoformat(byid[rid]['next_review_on'])>=today]
        if not valid:
            errors.append('Obiettivo senza fonti primarie verificate: '+o['id'])
    return errors


def local_links():
    errors = []
    for file in ROOT.rglob('*.md'):
        if any(x in file.parts for x in ('.cache','.git')):
            continue
        text = file.read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if target.startswith(('https://','http://','#','mailto:')):
                continue
            target = unquote(target.split('#')[0].strip('<>'))
            if target and not (file.parent / target).exists():
                errors.append(str(file.relative_to(ROOT))+': collegamento locale inesistente: '+target)
    return errors


def main():
    rows = assemble()
    errors = validate_data(rows, load('objectives.json'), load('observed-guide.json'), load('guide-structure.json'))
    errors += local_links()
    generated = load('catalog.json')
    if generated != rows:
        errors.append('Catalogo generato non aggiornato: eseguire python scripts/catalogue.py')
    expected = load('coverage.json')
    if expected['objectives'] != coverage(rows) or expected['as_of'] != rome_now().date().isoformat():
        errors.append('Matrice generata non aggiornata')
    if errors:
        print('\n'.join('ERRORE: '+e for e in errors))
        return 1
    kinds = Counter(r['kind'] for r in rows)
    total=len(load('objectives.json')['objectives'])
    print(f"OK: {len(rows)} record; {kinds['learn_path']} percorsi; {kinds['learn_module']} moduli; {kinds['learn_unit']} unità; {total}/{total} obiettivi con fonti primarie. Link locali e struttura verificati.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
