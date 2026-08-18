import tempfile
import unittest
from pathlib import Path

from scripts import release_audit


class ReleaseAuditTests(unittest.TestCase):
    def test_safe_text_file_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            safe = root / "README.md"
            safe.write_text("Synthetic research artifact.\n", encoding="utf-8")

            self.assertEqual(release_audit.audit_files(root, [safe]), [])

    def test_local_path_and_token_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            unsafe = root / "notes.txt"
            local_path = "/" + "Users/example/private"
            token = "github_" + "pat_1234567890abcdef"
            unsafe.write_text(
                f"{local_path} and {token}\n",
                encoding="utf-8",
            )

            findings = release_audit.audit_files(root, [unsafe])

            self.assertTrue(any("absolute local path" in item for item in findings))
            self.assertTrue(any("credential-like value" in item for item in findings))

    def test_private_validation_path_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            private = root / "validation" / "responses" / "participant.csv"
            private.parent.mkdir(parents=True)
            private.write_text("participant_id,response\n", encoding="utf-8")

            findings = release_audit.audit_files(root, [private])

            self.assertTrue(any("participant-data path" in item for item in findings))


if __name__ == "__main__":
    unittest.main()
