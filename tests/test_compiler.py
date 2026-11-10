import json
import os
import shutil
import tempfile
import unittest

from _charger import charger, exemple

plan = charger("fondateur-plan", "compiler")


class Compiler(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        with open(os.path.join(self.d, "idee.md"), "w", encoding="utf-8") as fh:
            fh.write("# Jus Lagune\n\nUn kiosque de jus naturels à Cocody Angré.\n")

    def tearDown(self):
        shutil.rmtree(self.d)

    def chiffres(self, **changement):
        with open(exemple("fondateur-finances", "exemple.json"), encoding="utf-8") as fh:
            s = json.load(fh)
        s.update(changement)
        with open(os.path.join(self.d, "chiffres.json"), "w", encoding="utf-8") as fh:
            json.dump(s, fh, ensure_ascii=False)

    def panel(self, achats, n=100):
        os.makedirs(os.path.join(self.d, "panel"), exist_ok=True)
        with open(os.path.join(self.d, "panel", "resultats.json"), "w", encoding="utf-8") as fh:
            json.dump({"achats": achats, "refus": n - achats, "repondu": n, "taux_achat": achats / float(n)}, fh)

    def test_sans_chiffres_incomplet(self):
        v, texte = plan.compiler_plan(self.d)
        self.assertEqual(v, "Incomplet")
        self.assertIn("lancez /fondateur-finances", texte)

    def test_bons_chiffres_et_panel_rentable(self):
        self.chiffres()
        self.panel(40)
        v, texte = plan.compiler_plan(self.d)
        self.assertEqual(v, "Rentable")
        self.assertTrue(texte.startswith("# Jus Lagune · Plan d'affaires"))
        self.assertIn("| Marge nette au volume visé | 34% par bouteille |", texte)
        self.assertIn("| Point d'équilibre | 34 bouteilles par jour |", texte)
        self.assertIn("40 achètent · 60 passent", texte)
        self.assertIn("- Le panel d'acheteurs : lancez /fondateur-panel", texte)

    def test_panel_faible_pas_encore(self):
        self.chiffres()
        self.panel(12)
        v, texte = plan.compiler_plan(self.d)
        self.assertEqual(v, "Pas encore")
        self.assertIn("✗ 12 acheteurs simulés sur 100 achètent", texte)

    def test_perte_par_unite_pas_encore(self):
        self.chiffres(prix=300)
        v, texte = plan.compiler_plan(self.d)
        self.assertEqual(v, "Pas encore")
        self.assertIn("PERD", texte)


if __name__ == "__main__":
    unittest.main()
