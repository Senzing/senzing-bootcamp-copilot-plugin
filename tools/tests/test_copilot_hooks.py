import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "plugins/senzing-bootcamp/scripts/copilot-hooks.py"


class CopilotHookTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.project = Path(temporary.name)
        (self.project / "config").mkdir()
        (self.project / "config/bootcamp_progress.json").write_text("{}", encoding="utf-8")

    def run_hook(self, event, payload):
        return subprocess.run(
            ["python3", str(HOOK), event],
            cwd=self.project,
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=False,
        )

    def test_pre_tool_denies_secret_in_write_content(self):
        result = self.run_hook("pre-tool", {
            "toolName": "write_file",
            "toolArgs": {"file_path": "notes.txt", "content": "AKIA1234567890ABCDEF"},
        })

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["permissionDecision"], "deny")

    def test_pre_tool_allows_ordinary_write_content(self):
        result = self.run_hook("pre-tool", {
            "tool_name": "write_file",
            "tool_input": {"file_path": "notes.txt", "content": "Ordinary synthetic note."},
        })

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_pre_tool_scans_apply_patch_text(self):
        result = self.run_hook("pre-tool", {
            "toolCalls": [{
                "name": "apply_patch",
                "args": "*** Begin Patch\n*** Add File: notes.txt\n+AKIA1234567890ABCDEF\n*** End Patch",
            }],
        })

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["permissionDecision"], "deny")

    def test_pre_tool_preserves_out_of_project_path_denial(self):
        result = self.run_hook("pre-tool", {
            "toolName": "write_file",
            "toolArgs": {
                "file_path": str(self.project.parent / "outside.txt"),
                "content": "Ordinary synthetic note.",
            },
        })

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["permissionDecision"], "deny")

    def test_stop_alias_payload_blocks_when_active_turn_has_no_question(self):
        transcript = self.project / "transcript.jsonl"
        transcript.write_text(
            "\n".join((
                json.dumps({"type": "user.message", "data": {"content": "Continue"}}),
                json.dumps({"type": "assistant.message", "data": {"content": "DONE"}}),
            )),
            encoding="utf-8",
        )

        result = self.run_hook("agent-stop", {
            "hook_event_name": "Stop",
            "stop_hook_active": False,
            "transcript_path": str(transcript),
        })

        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["decision"], "block")
        self.assertIn("closing question", output["reason"])

    def test_stop_alias_does_not_block_its_own_continuation(self):
        result = self.run_hook("agent-stop", {
            "hook_event_name": "Stop",
            "stop_hook_active": True,
            "transcript_path": str(self.project / "missing.jsonl"),
        })

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
