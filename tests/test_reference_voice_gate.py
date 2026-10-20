import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "wolof_tts" / "generate_reference_voice_batch.py"


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


if __name__ == "__main__":
    unittest.main()
