import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "wolof_plan_validator", ROOT / "wolof_tts" / "validate_wolof_batch_plan.py"
)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class WolofBatchPlanValidationTests(unittest.TestCase):
    def make_plan(self, path):
        subprocess.run([
            "python", str(ROOT / "wolof_tts" / "plan_next_audio_batch.py"),
            "--input-candidates", "data/kaikki-wolof-candidates.json",
            "--previous-manifest", "wolof_tts/manifests/historical-audio-headwords.json",
            "--batch-size", "10", "--start-offset", "0", "--output", str(path),
        ], cwd=ROOT, check=True, capture_output=True, text=True)

    def test_validator_normalization_collapses_whitespace_and_preserves_diacritics(self):
        self.assertEqual(VALIDATOR.norm("  Kër   bu   mag "), "kër bu mag")
        self.assertEqual(VALIDATOR.norm("Kër"), "kër")
        self.assertNotEqual(VALIDATOR.norm("Kër"), VALIDATOR.norm("Ker"))

    def test_real_planner_output_validates_without_tts_imports(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "plan.json"
            self.make_plan(plan)
            result = VALIDATOR.validate_plan(plan)
            self.assertTrue(result["valid"])
            self.assertEqual(result["selected_count"], 10)
            self.assertFalse(result["audio_generated"])
            self.assertFalse(result["tts_model_loaded"])
            generator_check = subprocess.run([
                "python", str(ROOT / "wolof_tts" / "generate_lexicon_batch.py"),
                "--plan-json", str(plan), "--validate-plan-only",
            ], cwd=ROOT, check=True, capture_output=True, text=True)
            self.assertFalse(json.loads(generator_check.stdout)["tts_model_loaded"])
            self.assertFalse(json.loads(generator_check.stdout)["audio_generated"])

    def test_changed_source_hash_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan_path = Path(tmp) / "plan.json"
            self.make_plan(plan_path)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan["source_hashes"]["kaikki_candidates_json_sha256"] = "0" * 64
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "does not match"):
                VALIDATOR.validate_plan(plan_path)

    def test_duplicate_selected_headword_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan_path = Path(tmp) / "plan.json"
            self.make_plan(plan_path)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan["selected"][1]["wolof"] = plan["selected"][0]["wolof"]
            plan["selected"][1]["french"] = plan["selected"][0]["french"]
            plan["selected_count"] = len(plan["selected"])
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate normalized"):
                VALIDATOR.validate_plan(plan_path)


if __name__ == "__main__":
    unittest.main()
