import json
import sys
import tempfile
import unittest
from pathlib import Path

from evals.runner import run_case, validate_case_document, validate_profile_document


class RunnerTests(unittest.TestCase):
    def test_command_adapter_runs_and_persists_evidence(self):
        case = {
            "id": "fake",
            "prompt": "Return the marker",
            "expectedHatSequence": [],
            "required": ["EVAL-OK"],
        }
        profile = {
            "command": sys.executable,
            "args": ["-c", "print('EVAL-OK')"],
            "timeoutMs": 5000,
            "metadata": {"treatment": "fake"},
        }
        with tempfile.TemporaryDirectory() as directory:
            result = run_case(case, "fake", profile, Path(directory), iteration=1)
            self.assertEqual(result["execution"]["exitCode"], 0)
            self.assertEqual(result["verification"]["status"], "passed")
            self.assertTrue(Path(result["artifacts"]["stdout"]).is_file())
            self.assertEqual(Path(result["artifacts"]["stdout"]).read_text().strip(), "EVAL-OK")
            self.assertFalse(result["execution"]["adapterFailure"])

    def test_command_adapter_detects_zero_exit_failure_marker(self):
        case = {"id": "fake-failure", "prompt": "x", "expectedHatSequence": []}
        profile = {
            "command": sys.executable,
            "args": ["-c", "print('API call failed after retries')"],
            "timeoutMs": 5000,
            "failureOutputPrefixes": ["API call failed"],
        }
        with tempfile.TemporaryDirectory() as directory:
            result = run_case(case, "fake", profile, Path(directory), iteration=1)
            self.assertEqual(result["execution"]["exitCode"], 0)
            self.assertTrue(result["execution"]["adapterFailure"])

    def test_case_document_validation_rejects_missing_id(self):
        with self.assertRaisesRegex(ValueError, "id"):
            validate_case_document({"schemaVersion": 1, "cases": [{"prompt": "x", "profiles": ["p"]}]})

    def test_profile_document_validation_rejects_shell_string_args(self):
        with self.assertRaisesRegex(ValueError, "args"):
            validate_profile_document(
                {"schemaVersion": 1, "profiles": {"p": {"command": "agent --flag", "args": "unsafe"}}}
            )


if __name__ == "__main__":
    unittest.main()
