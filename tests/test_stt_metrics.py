import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
from stt_metrics import (  # noqa: E402
    character_error_counts,
    edit_distance,
    normalize_text,
    word_error_counts,
)


class SttMetricsTests(unittest.TestCase):
    def test_unicode_and_whitespace_normalization_preserves_accents(self):
        self.assertEqual(normalize_text("  ÉCOLE  "), "école")
        self.assertEqual(normalize_text("e\u0301cole"), "école")

    def test_edit_distance(self):
        self.assertEqual(edit_distance("kitten", "sitting"), 3)
        self.assertEqual(edit_distance(["un", "test"], ["un", "texte"]), 1)

    def test_word_error_counts(self):
        self.assertEqual(word_error_counts("C'est un test", "C'est un texte"), (1, 3))

    def test_character_error_counts(self):
        self.assertEqual(character_error_counts("abc", "adc"), (1, 3))

    def test_empty_reference_is_rejected(self):
        with self.assertRaises(ValueError):
            word_error_counts("   ", "texte")
        with self.assertRaises(ValueError):
            character_error_counts("", "texte")


if __name__ == "__main__":
    unittest.main()
