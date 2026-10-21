import csv
import tempfile
import unittest
from pathlib import Path

from scripts.compare_lexique_dictionary import compare


class DictionaryComparisonTests(unittest.TestCase):
    def test_existing_lemma_is_flagged_for_enrichment_not_import(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project.csv"
            source = root / "source.csv"
            output = root / "review.csv"
            project.write_text(
                "id;soninke;francais;categorie;source;statut\n"
                "SNK-1;baane;un;nom;referent;fourni_par_referent\n",
                encoding="utf-8",
            )
            source.write_text(
                "lemme,variante,glose_extraite_automatiquement,texte_source,paragraphe_source,source\n"
                "baane,,seul,exemple source,39,Dictionnaire soninké.docx\n"
                "xala,,nouveau sens,autre exemple,40,Dictionnaire soninké.docx\n"
                "baane,,chacun,exemple 2,41,Dictionnaire soninké.docx\n",
                encoding="utf-8",
            )

            total, existing = compare(project, source, output)
            with output.open(encoding="utf-8-sig", newline="") as stream:
                rows = list(csv.DictReader(stream, delimiter=";"))

            self.assertEqual(total, 3)
            self.assertEqual(existing, 2)
            self.assertEqual(rows[0]["decision_provisoire"], "LEMME_EXISTANT_A_ENRICHIR_OU_FUSIONNER")
            self.assertEqual(rows[1]["decision_provisoire"], "LEMME_CANDIDAT_NOUVEAU_A_VALIDER")
            self.assertEqual(rows[0]["occurrences_lemme_dans_source"], "2")
            self.assertEqual(rows[2]["glose_extraite_automatiquement"], "chacun")
            self.assertIn("Dictionnaire soninké.docx", rows[2]["source"])


if __name__ == "__main__":
    unittest.main()
