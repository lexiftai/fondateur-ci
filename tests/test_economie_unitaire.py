import json
import math
import unittest

from _charger import charger, exemple

eco = charger("fondateur-finances", "economie_unitaire")


def spec():
    with open(exemple("fondateur-finances", "exemple.json"), encoding="utf-8") as fh:
        return json.load(fh)


class EconomieUnitaire(unittest.TestCase):
    def test_l_exemple_redonne_le_plan(self):
        a = eco.analyser(spec())
        self.assertAlmostEqual(a["contribution"], 540, places=6)
        self.assertEqual(round(a["marge_au_volume_cible"] * 100), 34)
        self.assertEqual(math.ceil(a["equilibre_par_jour"]), 34)
        self.assertEqual(round(a["resultat_an1"]), 5722440)
        self.assertEqual(a["demarrage"], 1505000)
        self.assertEqual(a["mois_de_retour"], 6)
        self.assertEqual(round(a["tresorerie_a_prevoir"]), 1555800)
        self.assertEqual(a["alertes"], [])

    def test_un_taux_suit_le_prix(self):
        s = spec()
        base = eco.analyser(s)["variable_par_unite"]
        plus_cher = eco.analyser(s, prix=2000)["variable_par_unite"]
        self.assertAlmostEqual(plus_cher - base, 10, places=6)  # 1% de 1 000 FCFA de plus

    def test_les_couts_en_hausse_touchent_aussi_les_taux(self):
        s = spec()
        s["couts_variables"] = [{"libelle": "commission", "taux": 0.3}]
        base, _, _, pire = [r for _, r in eco.sensibilite(s)]
        self.assertLess(pire["contribution"], base["contribution"])
        self.assertAlmostEqual(base["contribution"] - pire["contribution"], 1000 * 0.3 * 0.15, places=6)

    def test_un_taux_est_refuse_dans_les_charges_fixes(self):
        s = spec()
        s["charges_fixes_mensuelles"].append({"libelle": "commission", "taux": 0.05})
        with self.assertRaises(eco.ErreurChiffres):
            eco.analyser(s)

    def test_prix_sous_le_cout_variable_signale(self):
        s = spec()
        s["prix"] = 300
        a = eco.analyser(s)
        self.assertTrue(math.isinf(a["equilibre_par_jour"]))
        self.assertTrue(any("perd de l'argent" in f for f in a["alertes"]))

    def test_equilibre_au_dessus_de_la_capacite_signale(self):
        s = spec()
        s["capacite_par_jour"] = 30
        a = eco.analyser(s)
        self.assertTrue(any("capacité est de 30" in f for f in a["alertes"]))

    def test_les_et_si_vont_dans_le_bon_sens(self):
        base = eco.analyser(spec())
        moins_cher = eco.analyser(spec(), prix=base["prix"] * 0.9)
        moins = eco.analyser(spec(), volume=0.8)
        self.assertLess(moins_cher["resultat_an1"], base["resultat_an1"])
        self.assertGreater(moins_cher["equilibre_par_jour"], base["equilibre_par_jour"])
        self.assertLess(moins["resultat_an1"], base["resultat_an1"])
        self.assertEqual(len(eco.sensibilite(spec())), 4)

    def test_une_mauvaise_entree_est_refusee_pas_devinee(self):
        s = spec()
        s["montee_par_jour"] = [100] * 11
        with self.assertRaises(eco.ErreurChiffres):
            eco.analyser(s)
        s = spec()
        del s["prix"]
        with self.assertRaises(eco.ErreurChiffres):
            eco.analyser(s)
        s = spec()
        s["couts_variables"][0]["cout"] = "beaucoup"
        with self.assertRaises(eco.ErreurChiffres):
            eco.analyser(s)

    def test_le_rapport_cite_les_chiffres_cles(self):
        s = spec()
        texte = eco.rapport(s, eco.analyser(s))
        for attendu in ("540 FCFA", "34 bouteilles par jour", "**34%**", "5 722 440 FCFA", "au mois 6",
                        "(1% du prix)", "DGI"):
            self.assertIn(attendu, texte)

    def test_montant_a_la_francaise(self):
        self.assertEqual(eco.montant(1234567), "1 234 567 FCFA")
        self.assertEqual(eco.montant(-500.4), "-500 FCFA")
        self.assertEqual(eco.montant(2500, "GHS"), "2 500 GHS")


if __name__ == "__main__":
    unittest.main()
