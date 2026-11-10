import csv
import os
import tempfile
import unittest

from _charger import charger

vw = charger("fondateur-prix", "van_westendorp")


def lignes(n=40):
    out = []
    for i in range(n):
        k = i / float(n - 1)
        out.append((250 + 100 * k, 400 + 100 * k, 600 + 150 * k, 750 + 200 * k))
    return out


class Prix(unittest.TestCase):
    def test_points_ordonnes_et_dans_les_reponses(self):
        res = vw.analyser(lignes())
        p = res["points"]
        for k in ("PMC", "PME", "OPP", "IPP"):
            self.assertIsNotNone(p[k], k)
            self.assertTrue(250 <= p[k] <= 950, (k, p[k]))
        self.assertLess(p["PMC"], p["PME"])
        self.assertLessEqual(p["PMC"], p["OPP"])
        self.assertLessEqual(p["OPP"], p["PME"])

    def test_lignes_desordonnees_ou_incompletes_ecartees(self):
        d = tempfile.mkdtemp()
        chemin = os.path.join(d, "p.csv")
        with open(chemin, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh, delimiter=";")
            w.writerow(vw.CLES)
            for r in lignes(10):
                w.writerow(r)
            w.writerow((900, 400, 600, 800))   # trop bas au-dessus de la bonne affaire : désordre
            w.writerow((300, "", 600, 800))    # incomplète
        obtenu, ecartees = vw.lire(chemin)
        self.assertEqual((len(obtenu), ecartees), (10, 2))

    def test_montants_ecrits_comme_dans_un_tableur(self):
        self.assertEqual(vw._f("1 000"), 1000)
        self.assertEqual(vw._f("1.000"), 1000)
        self.assertEqual(vw._f("1,000"), 1000)
        self.assertEqual(vw._f("2 500 FCFA"), 2500)
        self.assertEqual(vw._f("2,5"), 2.5)
        self.assertIsNone(vw._f(""))

    def test_trop_peu_de_reponses_refuse(self):
        with self.assertRaises(vw.ErreurPrix):
            vw.analyser(lignes(4))

    def test_prix_ronds(self):
        self.assertEqual(vw.prix_ronds(730), [700, 750])
        self.assertEqual(vw.prix_ronds(1137), [1100, 1200])
        self.assertEqual(vw.prix_ronds(12300), [12000, 12500])
        self.assertEqual(vw.prix_ronds(1000), [1000])

    def test_le_rapport_place_le_prix(self):
        res = vw.analyser(lignes())
        self.assertIn("**dans** la fourchette acceptable", vw.rapport(res, 0, prix=650))
        self.assertIn("**au-dessus de** la fourchette acceptable", vw.rapport(res, 0, prix=4000))
        self.assertIn("Prix ronds à tester", vw.rapport(res, 0))


if __name__ == "__main__":
    unittest.main()
