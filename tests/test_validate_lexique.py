import csv
import tempfile
import unittest
from pathlib import Path

from scripts.validate_lexique import validate

COLUMNS = ["id", "soninke", "francais", "categorie", "source", "statut"]


def entry(entry_id: str, soninke: str) -> dict[str, str]:
    return {
        "id": entry_id,
        "soninke": soninke,
        "francais": "sens",
        "categorie": "nom",
        "source": "test",
        "statut": "a_verifier",
    }


def validate_rows(rows: list[dict[str, str]]) -> list[str]:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "lexique.csv"
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=COLUMNS, delimiter=";")
            writer.writeheader()
            writer.writerows(rows)
        errors, _warnings, _count = validate(path)
        return errors


class DuplicateHeadwordTests(unittest.TestCase):
    def test_duplicate_headword_is_rejected_even_with_case_and_spacing_changes(self):
        errors = validate_rows([
            entry("SNK-1", "kà"),
            entry("SNK-2", "  KÀ  "),
        ])
        self.assertTrue(any("lemme soninké dupliqué" in error for error in errors), errors)

    def test_diacritics_are_preserved_in_headword_comparison(self):
        errors = validate_rows([
            entry("SNK-1", "ka"),
            entry("SNK-2", "kà"),
        ])
        self.assertFalse(any("lemme soninké dupliqué" in error for error in errors), errors)

    def test_unicode_composition_is_normalized(self):
        errors = validate_rows([
            entry("SNK-1", "é"),
            entry("SNK-2", "e\u0301"),
        ])
        self.assertTrue(any("lemme soninké dupliqué" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
