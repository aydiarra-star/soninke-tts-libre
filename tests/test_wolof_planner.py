import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "wolof_planner", ROOT / "wolof_tts" / "plan_next_audio_batch.py"
)
PLANNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PLANNER)


class WolofPlannerTests(unittest.TestCase):
    def test_normalization_preserves_diacritics_and_collapses_spaces(self):
        self.assertEqual(PLANNER.norm("  Jërëjëf   "), "jërëjëf")
        self.assertNotEqual(PLANNER.norm("Kër"), PLANNER.norm("Ker"))

    def test_manifest_headwords_are_normalized_and_deduplicated(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            path.write_text(json.dumps({
                "entries": [
                    {"wolof": "Kër"},
                    {"wolof": "  kër  "},
                    {"word": "Ñëw"},
                    {"wolof": ""},
                ]
            }), encoding="utf-8")
            words, digest = PLANNER.manifest_words(path)
            self.assertEqual(words, {"kër", "ñëw"})
            self.assertEqual(len(digest), 64)

    def test_unknown_manifest_shape_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            path.write_text('{"unexpected": []}', encoding="utf-8")
            with self.assertRaises(SystemExit):
                PLANNER.manifest_words(path)


if __name__ == "__main__":
    unittest.main()
