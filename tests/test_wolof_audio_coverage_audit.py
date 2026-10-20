import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "wolof_tts" / "audit_wolof_audio_coverage.py"
SPEC = importlib.util.spec_from_file_location("audit_wolof_audio_coverage", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class WolofAudioCoverageAuditTests(unittest.TestCase):
    def test_only_reference_hashed_verified_voice_counts_as_verified(self):
        lexicon = {"entries": [
            {"wolof": {"word": "Jërëjëf"}, "fr": {"word": "Merci"}},
            {"wolof": {"word": "Kër"}, "fr": {"word": "Maison"}},
            {"wolof": {"word": "Ñëw"}, "fr": {"word": ""}},
        ]}
        manifest = {"entries": [
            {"wolof": "Jërëjëf", "model": "OmniVoice", "voice_identity_validation": "verified",
             "reference_audio_sha256": "abc"},
            {"wolof": "Kër", "model": "Adia_TTS", "voice_identity_validation": "pending"},
            {"wolof": "mot-inconnu", "model": "Adia_TTS", "translation_validation": "unverified-candidate"},
        ]}
        report = MODULE.build_report(lexicon, manifest)
        self.assertEqual(report["dictionary_entry_rows"], 3)
        self.assertEqual(report["dictionary_unique_wolof_forms"], 3)
        self.assertEqual(report["dictionary_forms_missing_french_translation"], ["ñëw"])
        self.assertEqual(report["dictionary_forms_with_audio_manifest"], 2)
        self.assertEqual(report["dictionary_forms_with_verified_reference_voice"], 1)
        self.assertEqual(report["dictionary_forms_with_voice_identity_pending_or_unverified"], 1)
        self.assertEqual(report["dictionary_forms_without_audio_manifest"], 1)
        self.assertEqual(report["audio_headwords_not_in_dictionary"], ["mot-inconnu"])
        self.assertEqual(report["audio_headwords_with_translation_review_flags"], ["mot-inconnu"])

    def test_unhashed_voice_never_counts_as_verified(self):
        report = MODULE.build_report(
            {"entries": [{"wolof": {"word": "Jërëjëf"}, "fr": {"word": "Merci"}}]},
            {"entries": [{"wolof": "Jërëjëf", "voice_identity_validation": "verified"}]},
        )
        self.assertEqual(report["dictionary_forms_with_verified_reference_voice"], 0)

    def test_duplicate_form_is_not_missing_french_if_any_variant_has_translation(self):
        report = MODULE.build_report(
            {"entries": [
                {"wolof": {"word": "Jërëjëf"}, "fr": {"word": ""}},
                {"wolof": {"word": "JËRËJËF"}, "fr": {"word": "Merci"}},
            ]},
            {"entries": []},
        )
        self.assertEqual(report["dictionary_entry_rows"], 2)
        self.assertEqual(report["dictionary_unique_wolof_forms"], 1)
        self.assertEqual(report["dictionary_forms_with_french_translation"], 1)
        self.assertEqual(report["dictionary_forms_missing_french_translation"], [])


if __name__ == "__main__":
    unittest.main()
