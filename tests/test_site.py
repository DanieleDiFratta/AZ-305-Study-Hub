"""Protect personal evidence and the public artifact boundary of the dashboard."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_site import BLOCK_IDS, build, curriculum, materials, markdown, read_json, validate_progress
from catalogue import assemble, load


class StaticDashboard(unittest.TestCase):
    def setUp(self):
        self.baseline = load('objectives.json')
        self.progress = read_json(ROOT / 'studio/progressi.json')

    def test_curriculum_preserves_every_objective_and_official_learn_order(self):
        resources = {r['id']: r for r in assemble()}
        blocks = curriculum(self.baseline['objectives'], resources)
        covered = {oid for b in blocks for oid in b['objective_ids']}
        self.assertEqual(covered, {o['id'] for o in self.baseline['objectives']})
        self.assertEqual([b['id'] for b in blocks], BLOCK_IDS)
        self.assertEqual([resources[b['id']]['source_uid'] for b in blocks], resources['EXAM-COURSE']['syllabus_path_uids'])
        self.assertTrue(all(b['resource_ids'] for b in blocks))
        for block in blocks:
            self.assertEqual([m['id'] for m in block['modules']], resources[block['id']]['module_ids'])
            for module in block['modules']:
                self.assertEqual(module['unit_ids'], resources[module['id']]['unit_ids'])
        self.assertIn('1.2.4', next(b for b in blocks if b['id'] == 'LP-IDENTITY')['objective_ids'])
        self.assertEqual(len({m['id'] for b in blocks for m in b['modules']}), 23)
        self.assertEqual(len({uid for b in blocks for m in b['modules'] for uid in m['unit_ids']}), 206)

    def test_progress_requires_real_evidence_and_known_ids(self):
        cases = [({'read': True}, '1.1.1'), ({'verified': {'on': '2026-10-15', 'evidence': ''}}, '1.1.1'),
                 ({'read': {'on': '2026-10-15', 'evidence': 'Dichiarazione'}}, '9.9.9')]
        for flags, oid in cases:
            with self.subTest(oid=oid, flags=flags):
                candidate = copy.deepcopy(self.progress)
                candidate['objectives'][oid] = flags
                with self.assertRaises((ValueError, KeyError)):
                    validate_progress(candidate, self.baseline['objectives'])

    def test_verification_does_not_invent_reading_or_exercise(self):
        self.progress['objectives']['1.1.1'] = {'verified': {'on': '2026-10-15', 'evidence': 'Ragionamento valutato'}}
        validate_progress(self.progress, self.baseline['objectives'])
        self.assertEqual(set(self.progress['objectives']['1.1.1']), {'verified'})

    def test_build_is_read_only_and_publishes_only_explicit_assets(self):
        source_paths = list((ROOT / 'data').glob('*.json')) + [ROOT / 'studio/progressi.json', ROOT / 'studio/materiali.json']
        before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            payload = build(output)
            self.assertEqual({p.name for p in output.iterdir()}, {'index.html', 'app.js', 'style.css', 'favicon.svg', 'site-data.js', '.nojekyll'})
            self.assertEqual(len(payload['resources']), len(assemble()))
            self.assertEqual(payload['progress'], self.progress)
            self.assertNotIn('response_sha256', (output / 'site-data.js').read_text(encoding='utf-8'))
            self.assertTrue((output / 'site-data.js').read_text(encoding='utf-8').startswith('window.STUDY_DATA='))
        self.assertEqual(before, {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths})

    def test_manifest_cannot_publish_repository_files(self):
        entry = {'id': 'test', 'kind': 'notes', 'title': 'Test', 'block_id': 'LP-IDENTITY', 'published_on': '2026-10-15', 'path': 'data/reviews.json'}
        with self.assertRaises(ValueError):
            materials({'schema_version': 1, 'items': [entry]})

    def test_material_rendering_and_flashcards(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'studio/ripasso') as directory:
            folder = Path(directory)
            (folder / 'note.md').write_text('# Titolo\nTesto **originale**.\n- Punto\n<script>alert(1)</script>', encoding='utf-8')
            (folder / 'cards.json').write_text(json.dumps([{'question': 'Domanda di prova', 'answer': 'Risposta di prova'}]), encoding='utf-8')
            (folder / 'map.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><title>Prova</title><text x="5" y="20">Nodo</text></svg>', encoding='utf-8')
            entries = [{'id': kind, 'kind': kind, 'title': 'Fixture di test', 'block_id': 'LP-PREREQ', 'published_on': '2026-10-15', 'path': str((folder / filename).relative_to(ROOT))} for kind, filename in [('notes', 'note.md'), ('flashcards', 'cards.json'), ('map', 'map.svg')]]
            result = materials({'schema_version': 1, 'items': entries})
            self.assertIn('<strong>originale</strong>', result[0]['html'])
            self.assertNotIn('<script>', result[0]['html'])
            self.assertEqual(result[1]['cards'][0]['answer'], 'Risposta di prova')
            self.assertIn('viewBox', result[2]['html'])
            (folder / 'map.svg').write_text('<svg viewBox="0 0 1 1" onload="alert(1)"/>', encoding='utf-8')
            with self.assertRaises(ValueError):
                materials({'schema_version': 1, 'items': [entries[2]]})

    def test_markdown_does_not_execute_html_or_script_links(self):
        html = markdown('<img src=x onerror=alert(1)>\n[Link](javascript:alert)\n[Microsoft](https://learn.microsoft.com/)')
        self.assertNotIn('<img', html)
        self.assertNotIn('href="javascript:', html)
        self.assertIn('href="https://learn.microsoft.com/"', html)


if __name__ == '__main__':
    unittest.main()
