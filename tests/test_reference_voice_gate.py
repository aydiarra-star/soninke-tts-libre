import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "wolof_tts" / "generate_reference_voice_batch.py"
SPEC = importlib.util.spec_from_file_location("generate_reference_voice_batch", SCRIPT)
GENERATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GENERATOR)


class ReferenceVoiceGateTests(unittest.TestCase):
    def run_script(self, *args):
        env = os.environ.copy()
        env.pop("WOLOF_REFERENCE_AUDIO_B64", None)
        env.pop("WOLOF_REFERENCE_TRANSCRIPT", None)
        with tempfile.TemporaryDirectory() as out:
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--output-dir", out, *args],
                cwd=ROOT, env=env, text=True, capture_output=True, timeout=20,
            )
        return result

    def test_generator_requests_wolof_language_id(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('"language": "wo"', source)
        self.assertNotIn('"language": "wo"', source)

    def test_missing_reference_fails_closed(self):
        result = self.run_script("--poc-text", "Jërëjëf")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOQUÉ", result.stderr + result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_batch_requires_human_voice_approval(self):
        result = self.run_script("--batch")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("validation humaine", result.stderr + result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    
    def test_every_dictionary_entry_is_retained_even_when_headword_repeats(self):
        lexicon = {"entries": [
            {"id": "sense-1", "wolof": {"word": "Jërëjëf"}, "fr": {"word": "Merci"},
             "translationStatus": "source-documented"},
            {"id": "sense-2", "wolof": {"word": "JËRËJËF"}, "fr": {"word": "Remerciements"},
             "translationStatus": "source-documented"},
        ]}
        rows = GENERATOR.select_entries(0, 10, lexicon_payload=lexicon, manifest_payload={"entries": []})
        self.assertEqual([row["entry_id"] for row in rows], ["sense-1", "sense-2"])
        self.assertEqual(len(rows), 2)

    def test_uncertain_dictionary_or_audio_translation_is_excluded(self):
        lexicon = {"entries": [
            {"id": "review-dict", "wolof": {"word": "mot-a"}, "fr": {"word": "traduction A"},
             "translationStatus": "unverified-candidate"},
            {"id": "review-audio", "wolof": {"word": "mot-b"}, "fr": {"word": "traduction B"},
             "translationStatus": "source-documented"},
            {"id": "eligible", "wolof": {"word": "mot-c"}, "fr": {"word": "traduction C"},
             "translationStatus": "source-documented"},
        ]}
        manifest = {"entries": [
            {"wolof": "mot-b", "translation_validation": "unverified-candidate"},
        ]}
        rows = GENERATOR.select_entries(0, 10, lexicon_payload=lexicon, manifest_payload=manifest)
        self.assertEqual([row["entry_id"] for row in rows], ["eligible"])


if __name__ == "__main__":
    unittest.main()
