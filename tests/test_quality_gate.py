"""Regression checks: failures must not silently produce a complete collection."""
from datetime import date
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from catalogue import assemble, load
from validate import validate_data


class QualityGate(unittest.TestCase):
    def setUp(self):
        self.rows = assemble()
        self.baseline = load('objectives.json')
        self.observed = load('observed-guide.json')
        self.accepted = load('guide-structure.json')
        self.today = date(2026,10,15)

    def errors(self):
        return validate_data(self.rows,self.baseline,self.observed,self.accepted,self.today)

    def test_missing_objective_is_detected(self):
        self.baseline['objectives'].pop()
        self.assertTrue(any('Elenco obiettivi incompleto' in e for e in self.errors()))

    def test_all_primary_sources_missing_cannot_pass(self):
        for r in self.rows:
            if r['review']['coverage_role']=='primary':
                r['objective_ids'] = [oid for oid in r['objective_ids'] if oid!='4.1.5']
        self.assertIn('Obiettivo senza fonti primarie verificate: 4.1.5',self.errors())

    def test_changed_bullet_same_count_requires_review(self):
        self.observed['groups']['1.1']['bullet_sha256'][0]='changed'
        self.assertTrue(any('testo dei bullet' in e for e in self.errors()))

    def test_changed_response_requires_review(self):
        self.rows[0]['access']['response_sha256']='changed'
        self.assertTrue(any('risposta cambiata' in e for e in self.errors()))

    def test_unlisted_unit_is_detected(self):
        m=next(r for r in self.rows if r['kind']=='learn_module')
        m['unit_ids'].pop()
        self.assertTrue(any('numero unità' in e or 'unità orfana' in e for e in self.errors()))

    def test_expired_sources_do_not_pass(self):
        self.today=date(2027,1,1)
        self.assertTrue(any('verifica scaduta' in e for e in self.errors()))

    def test_http_200_with_no_content_is_not_accepted(self):
        r=next(r for r in self.rows if r['id']=='COMP-BATCH')
        r['access']['status']='content_not_available'
        self.assertIn('Obiettivo senza fonti primarie verificate: 4.1.5',self.errors())


if __name__=='__main__':
    unittest.main()
