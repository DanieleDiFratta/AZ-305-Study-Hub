"""Editorial mappings and generated, auditable catalog. No network requests.

--record-review records an editorial review of the current cached response hashes.
Run it only after inspecting changed sources; normal rendering never approves changes.
"""
import argparse
from collections import Counter
from datetime import date
import json

from inspect_source import ROOT
from research import rome_now, write

DATA = ROOT / 'data'
DOCS = ROOT / 'docs'

UNIT_MAP = {
 'design-governance': {2:'1.3.1 1.3.2',3:'1.3.1',4:'1.3.1',5:'1.3.1',6:'1.3.1',7:'1.3.2',8:'1.2.3',9:'1.3.1'},
 'design-authentication-authorization-solutions': {2:'1.2.1 1.2.2',3:'1.2.1 1.2.2',4:'1.2.1 1.2.2',5:'1.2.1 1.2.2',6:'1.2.1',7:'1.2.2',8:'1.3.3',9:'1.2.2 1.2.3',10:'1.2.2 1.2.3',11:'1.2.5'},
 'design-solution-to-log-monitor-azure-resources': {2:'1.1.1 1.1.2 1.1.3',3:'1.1.1',4:'1.1.3',5:'1.1.1'},
 'design-data-storage-solution-for-relational-data': {2:'2.1.1 2.1.2',3:'2.1.1 2.1.2',4:'2.1.1 2.1.2',5:'2.1.3',6:'3.2.2',7:'2.1.4',8:'2.2.1'},
 'design-data-storage-solution-for-non-relational-data': {2:'2.2.2 2.2.3',3:'2.2.2 2.2.3',4:'2.2.4 3.2.3',5:'2.2.2 2.2.3',6:'2.2.2 2.2.3',7:'2.2.2 2.2.3',8:'2.2.4'},
 'design-data-integration': {2:'2.3.1',3:'2.3.1 2.3.2',4:'2.3.1 2.3.2',5:'2.3.1 2.3.2',6:'2.3.1 2.3.2',7:'2.3.2'},
 'describe-high-availability-disaster-recovery-strategies': {2:'3.1.1',3:'3.1.1 3.2.1 3.2.2 3.2.3',4:'3.2.1',5:'3.2.1 3.2.2 3.2.3',6:'3.2.1',7:'3.1.1'},
 'design-solution-for-backup-disaster-recovery': {2:'3.1.1',3:'3.1.1 3.1.2 3.1.3 3.1.4',4:'3.1.4',5:'3.1.4',6:'3.1.2',7:'3.1.3',8:'3.1.1 3.1.2'},
 'design-compute-solution': {2:'4.1.1',3:'4.1.2',4:'4.1.5',5:'4.1.1',6:'4.1.3',7:'4.1.3',8:'4.1.4',9:'4.1.4'},
 'design-application-architecture': {2:'4.2.1 4.2.2',3:'4.2.1',4:'4.2.2',5:'4.2.2',6:'4.2.4',7:'4.2.3',8:'4.2.6',9:'4.2.5'},
 'design-migrations': {2:'4.3.1',3:'4.3.1 4.3.2',4:'4.3.2',5:'4.3.3',6:'4.3.4',7:'4.3.5',8:'4.3.5'},
 'design-network-solutions': {2:'4.4.1 4.4.2',3:'4.4.2',4:'4.4.1 4.4.5',5:'4.4.2',6:'4.4.5',7:'4.4.5 4.4.3',8:'4.4.4'},
}
CONTEXT = {
 'describe-core-architectural-components-of-azure':'1.3.1 3.2.1',
 'describe-azure-compute-networking-services':'4.1.1 4.1.2 4.1.3 4.1.4 4.4.1 4.4.2',
 'describe-azure-storage-services':'2.2.2 2.2.3 2.2.4 4.3.5',
 'describe-azure-identity-access-security':'1.2.1 1.2.2 1.2.3 1.3.3',
 'cloud-adoption-framework':'1.3.1 1.3.2 4.3.1',
 'azure-well-architected-reliability':'3.1.1 3.1.2 3.1.3 3.1.4 3.2.1 3.2.2 3.2.3',
 'azure-well-architected-security':'1.2.1 1.2.3 1.2.5 2.1.4 2.2.4 4.4.4',
 'azure-well-architected-cost-optimization':'2.1.2 2.2.3 4.1.1',
 'azure-well-architected-performance-efficiency':'2.1.3 4.1.1 4.4.3',
 'azure-well-architected-operational-excellence':'1.1.1 1.1.3 4.2.6',
}
CASES = {
 'LAB-01':'1.3.1 1.3.2', 'LAB-02':'4.1.1 4.1.2 4.1.3 4.1.4 4.1.5',
 'LAB-03':'2.2.1 2.2.2 2.2.3 2.2.4', 'LAB-04':'2.1.1 2.1.2 2.1.3 2.1.4',
 'LAB-06':'4.2.1 4.2.2 4.2.3 4.2.4 4.2.5 4.2.6',
 'LAB-07':'1.2.1 1.2.2 1.2.3 1.2.5',
 'LAB-08':'1.1.1 1.1.2 1.1.3 1.3.1 2.1.1 2.2.1 4.1.1 4.2.1',
 'LAB-09':'4.4.1 4.4.2 4.4.3 4.4.4 4.4.5',
}


def load(name):
    return json.loads((DATA / name).read_text(encoding='utf-8'))


def raw_rows():
    return load('resources.json') + load('extra-resources.json')


def guide_structure(rows):
    return load('observed-guide.json')


def record():
    rows = raw_rows()
    all_ids = [o['id'] for o in load('objectives.json')['objectives']]
    CONTEXT['azure-well-architected-introduction'] = ' '.join(all_ids)
    reviews = {}
    modules = {r['id']: r for r in rows if r['kind'] == 'learn_module'}
    for mid, module in modules.items():
        slug = mid[2:]
        maps = UNIT_MAP.get(slug, {})
        mapped = sorted({o for value in maps.values() for o in value.split()}) or CONTEXT.get(slug, '').split()
        module['objective_ids'] = mapped
    for r in rows:
        kind = r['kind']
        mapped = r['objective_ids']
        role = 'support'
        scope = r.get('mapping_scope', 'reference')
        note = r.get('selection_reason_it', '')
        if kind in ('documentation', 'comparison'):
            role = 'primary'
        if kind == 'learn_module':
            mapped, scope = modules[r['id']]['objective_ids'], 'module_context'
        if kind == 'learn_unit':
            slug = r['module_id'][2:]
            maps = UNIT_MAP.get(slug, {})
            mapped = maps.get(r['unit_order'], '').split()
            if mapped:
                scope, role = 'direct', 'training'
                note = 'Unità tematica allineata agli obiettivi indicati; inventario di pertinenza, non studio completato.'
            else:
                mapped, scope = modules[r['module_id']]['objective_ids'], 'module_context'
                note = 'Contesto del modulo: introduzione, sintesi, assessment o prerequisito; non prova autonoma di copertura.'
        if kind in ('exam_guide', 'exam', 'course'):
            mapped, scope = all_ids, 'reference'
        if kind == 'learn_path':
            mapped = sorted({o for mid in r['module_ids'] for o in modules[mid]['objective_ids']})
            scope = 'path_context'
        if r['id'] in CASES:
            mapped, scope = CASES[r['id']].split(), 'case_context'
            note = 'Caso utile per gli obiettivi indicati nel loro insieme; non certifica ogni sottorequisito o ogni feature attuale.'
        flags = []
        if r['id'] in ('LAB-05', 'LAB-10', 'LAB-11'):
            flags.append('no_formal_case_study')
            mapped, scope = [], 'placeholder'
        if r['id'] == 'LAB-12':
            mapped, scope = [], 'optional_outside_explicit_exam_bullets'
        if r['id'] in ('U-design-authentication-authorization-solutions-05', 'U-describe-azure-identity-access-security-04'):
            flags.append('compare_b2c_external_id_with_current_docs')
        if r['id'] == 'U-design-application-architecture-06':
            flags.append('redis_retirement_dates_require_current_faq')
        if r['id'] == 'U-design-network-solutions-04':
            flags.append('outbound_defaults_depend_on_api_version')
        if kind in ('official_case', 'customer_story'):
            flags.append('scenario_not_current_product_specification')
        reviews[r['id']] = {'reviewed_on': rome_now().date().isoformat(),
            'reviewed_response_sha256': r['access'].get('response_sha256'),
            'objective_ids': mapped, 'mapping_scope': scope, 'coverage_role': role,
            'review_depth': 'relevance_and_structure' if kind in ('learn_unit','learn_module','learn_path','official_case') else 'relevance_and_targeted_sections',
            'locator': 'H1: ' + r['title'], 'note_it': note, 'flags': flags}
    write('reviews.json', reviews)
    write('guide-structure.json', guide_structure(rows))


def assemble():
    reviews = load('reviews.json')
    rows = []
    for raw in raw_rows():
        r = {k:v for k,v in raw.items() if k not in ('outgoing_relevant_links','title_hint','content_review','review_status','images')}
        review = reviews.get(r['id'])
        r['review'] = review
        r['objective_ids'] = review['objective_ids'] if review else []
        r['mapping_scope'] = review['mapping_scope'] if review else 'unreviewed'
        r['review_current'] = bool(review and review.get('reviewed_response_sha256') and
                                   review['reviewed_response_sha256'] == r['access'].get('response_sha256'))
        r['fresh'] = date.fromisoformat(r['next_review_on']) >= rome_now().date()
        if r.get('exercise_status') == 'no_formal_case_study' and r['access'].get('http_status') == 200 and r['title'] == 'No formal case study':
            r['access'] = {**r['access'], 'status':'public_placeholder'}
        r['eligible_for_coverage'] = (r['access']['status'] in ('public_content', 'public_asset') and
                                      r['review_current'] and r['fresh'])
        rows.append(r)
    return sorted(rows, key=lambda r:r['id'])


def coverage(rows, objectives=None):
    result = []
    for objective in objectives if objectives is not None else load('objectives.json')['objectives']:
        oid = objective['id']
        sources = [r for r in rows if oid in r['objective_ids'] and r['eligible_for_coverage']]
        primary = [r['id'] for r in sources if r['review']['coverage_role'] == 'primary' and r['mapping_scope'] == 'direct']
        training = [r['id'] for r in sources if r['review']['coverage_role'] == 'training' and r['mapping_scope'] == 'direct']
        supporting = [r['id'] for r in sources if r['review']['coverage_role'] == 'support' and r['mapping_scope'] in ('direct','support','case_context')]
        result.append({**objective, 'primary_resource_ids':primary, 'training_unit_ids':training,
                       'supporting_resource_ids':supporting, 'verified_coverage':bool(primary),
                       'learn_gap':not training})
    return result


def link(r):
    return '[' + r['id'] + '](' + r['url'].replace(' ', '%20') + ')'


def save_doc(name, text):
    DOCS.mkdir(exist_ok=True)
    (DOCS / name).write_text(text.rstrip() + '\n', encoding='utf-8')


def render():
    rows = assemble()
    matrix = coverage(rows)
    byid = {r['id']:r for r in rows}
    write('catalog.json', rows)
    write('coverage.json', {'as_of':rome_now().date().isoformat(), 'definition':'at_least_one_reviewed_fresh_direct_primary_source',
                           'covered':sum(o['verified_coverage'] for o in matrix), 'total':len(matrix), 'objectives':matrix})
    lines = ['# Matrice di copertura AZ-305', '',
             'Baseline: **17 aprile 2026**. Le etichette sono parafrasi originali concise: il testo Microsoft integrale resta nella [Study Guide]('+ byid['EXAM-GUIDE']['url'] +'). Sezione e posizione del bullet sono conservate nei dati.', '',
             f"Verifica: **{rome_now().date().isoformat()}**. Copertura documentale: **{sum(o['verified_coverage'] for o in matrix)}/{len(matrix)}**. Una fonte deve essere pubblica, pertinente, revisionata sullo stesso hash e non scaduta. Fonti generiche, assessment, placeholder e soli diagrammi non chiudono un obiettivo.", '',
             'La copertura riguarda la biblioteca, non la preparazione personale. Tutti gli obiettivi personali sono `not_started`.', '']
    for domain in load('objectives.json')['domains']:
        lines += ['## '+domain['label_it']+' ('+domain['weight']+')','',
                  '| ID / obiettivo | Documentazione primaria | Unità Learn pertinenti | Stato |',
                  '| --- | --- | --- | --- |']
        for o in matrix:
            if o['domain'] != domain['id']:
                continue
            primary = ', '.join(link(byid[rid]) for rid in o['primary_resource_ids'])
            training = ', '.join(link(byid[rid]) for rid in o['training_unit_ids']) or 'Lacuna Learn: usare documentazione primaria'
            lines.append(f"| [{o['id']} — {o['label_it']}]({o['source_url']}) | {primary or 'MANCANTE'} | {training} | {'Fonte verificata' if o['verified_coverage'] else 'SCOPERTO'} |")
        lines.append('')
    lines += ['## Limiti della matrice','',
              'Ogni ID `a.b.c` corrisponde al bullet `c` della sezione `a.b`; non è una numerazione ufficiale Microsoft. Le sorgenti dei dati sono [objectives.json](../data/objectives.json), [reviews.json](../data/reviews.json) e [coverage.json](../data/coverage.json).', '',
              'Le unità introduttive e di sintesi ereditano solo il contesto del modulo. L’accesso on-premises (1.2.4) ha fonti documentali verificate, ma manca un’unità dedicata nei percorsi censiti. Per gli approfondimenti vedere [lacune e aggiornamenti](LACUNE-E-AGGIORNAMENTI.md).']
    save_doc('MATRICE-COPERTURA.md', '\n'.join(lines))
    kinds = Counter(r['kind'] for r in rows)
    bib = ['# Biblioteca delle fonti', '',
           f"Catalogo verificato il {rome_now().date().isoformat()}: {len(rows)} record, inclusi tre placeholder esplicitamente segnalati. Le 206 unità sono elencate separatamente in [PERCORSI-LEARN.md](PERCORSI-LEARN.md); ogni record completo è in [catalog.json](../data/catalog.json).", '',
           'Tutti i titoli delle pagine sono rilevati dalla fonte. I criteri di selezione e le associazioni agli obiettivi sono redazionali. Lingua `en-us` scelta come baseline; le traduzioni italiane non sono state verificate. `public_content` significa corpo leggibile tramite GET anonimo, non esecuzione di laboratori, video o funzioni autenticati.', '']
    for kind in sorted(kinds):
        if kind in ('learn_unit','learn_module'):
            continue
        bib += ['## '+kind,'','| ID / titolo | Obiettivi (o contesto) | Lingua | Verifica / accesso | Prossimo controllo |','| --- | --- | --- | --- | --- |']
        for r in rows:
            if r['kind'] == kind:
                bib.append(f"| <a id=\"{r['id'].lower()}\"></a>[{r['id']} — {r['title']}]({r['url'].replace(' ', '%20')}) | {', '.join(r['objective_ids']) or 'Riferimento / fuori obiettivi espliciti'} ({r['mapping_scope']}) | {r['language']} | {r['verified_on']} / {r['access']['status']} (HTTP {r['access'].get('http_status')}) | {r['next_review_on']} |")
        bib.append('')
    save_doc('BIBLIOTECA.md', '\n'.join(bib))
    learn = ['# Percorsi, moduli e unità Microsoft Learn','',
             'Perimetro: tutti i sei percorsi del syllabus AZ-305T00, verificati sul contenuto e sui metadati `learn_item` della pagina ufficiale. Non è un censimento di tutto Microsoft Learn. Ogni URL di modulo e unità è stato scoperto dall’indice del genitore e richiesto singolarmente.', '',
             'Sei percorsi, 23 moduli unici, 206 unità uniche. Il modulo introduttivo WAF appartiene a due percorsi ed è catalogato una sola volta. Le associazioni `module_context` e `path_context` sono contesto, non copertura atomica. Gli assessment non sono stati svolti; il login può essere necessario per risultati e progressi.', '']
    for p in [r for r in rows if r['kind']=='learn_path']:
        learn += ['## '+p['id']+' — '+p['title'],'', '[Percorso ufficiale]('+p['url']+') — '+str(len(p['module_ids']))+' moduli; '+p['language']+'; verificato '+p['verified_on']+'; '+p['access']['status']+'.', '']
        for mid in p['module_ids']:
            m = byid[mid]
            learn += ['### '+m['title'],'',link(m)+' — '+str(len(m['unit_ids']))+' unità; '+m['language']+'; '+m['verified_on']+'; '+m['access']['status']+'.', '',
                      '| Ordine | Unità | Obiettivi / contesto | Accessibilità / verifica |','| --- | --- | --- | --- |']
            for uid in m['unit_ids']:
                u = byid[uid]
                learn.append(f"| {u['unit_order']} | [{u['title']}]({u['url']}) (`{uid}`) | {', '.join(u['objective_ids'])} ({u['mapping_scope']}) | {u['access']['status']} / {u['verified_on']} / {u['language']} |")
            learn.append('')
    save_doc('PERCORSI-LEARN.md', '\n'.join(learn))
    summary = {'verified_on':rome_now().date().isoformat(), 'records':len(rows), 'by_kind':dict(kinds),
               'access_status':dict(Counter(r['access']['status'] for r in rows)),
               'objectives':len(matrix), 'covered':sum(o['verified_coverage'] for o in matrix),
               'missing_primary_sources':[o['id'] for o in matrix if not o['verified_coverage']],
               'learn_gaps':[o['id'] for o in matrix if o['learn_gap']],
               'changed_since_review':[r['id'] for r in rows if not r['review_current']],
               'due_for_review':[r['id'] for r in rows if not r['fresh']]}
    write('audit-summary.json', summary)
    print(json.dumps(summary, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--record-review', action='store_true')
    args = parser.parse_args()
    if args.record_review:
        record()
    render()
