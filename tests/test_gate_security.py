import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from brief_io import BriefError, load_brief, write_brief
from hard_gate import violations_of, write_record


class GateSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "compliance.yaml"
        self.brief = yaml.safe_load((ROOT / "fixtures/ok-brief.yaml").read_text())
        self.path.write_text(yaml.safe_dump(self.brief))

    def cli(self, *args, policy="block"):
        return subprocess.run([sys.executable, str(ROOT / "tools/hard_gate.py"), "--brief", str(self.path), *args],
                              env={**os.environ, "EU_COMPLIANCE_POLICY": policy}, capture_output=True, text=True)

    def test_unknown_environment_policy_cannot_turn_block_into_warn(self):
        self.brief["findings"][1]["certainty"] = 95
        self.path.write_text(yaml.safe_dump(self.brief))
        self.assertEqual(self.cli(policy="typo").returncode, 2)
        self.assertEqual(self.cli().returncode, 2)
        self.assertEqual(self.cli("--policy", "warn").returncode, 0)
        self.assertEqual(self.cli("--policy", "warn", policy="typo").returncode, 0)
        self.assertEqual(self.cli("--policy", "block", policy="typo").returncode, 2)

    def test_duplicate_keys_and_aliases_are_rejected(self):
        for text in [self.path.read_text() + "\ncertainty: 100\n", "x: &a [1]\ny: *a\n"]:
            self.path.write_text(text)
            with self.assertRaises(BriefError):
                load_brief(self.path)

    def test_malformed_and_oversized_briefs_fail_without_echoing_sensitive_data(self):
        for text in ["null", "[]", "secret: [private-value", "x" * (1024 * 1024 + 1)]:
            self.path.write_text(text)
            result = self.cli()
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("private-value", result.stdout + result.stderr)
            self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_malformed_source_is_rejected_before_engine_runs(self):
        self.brief["findings"][0]["source"] = "private-value"
        self.path.write_text(yaml.safe_dump(self.brief))
        self.assertEqual(self.cli().returncode, 2)

    def test_record_write_is_private_atomic_and_idempotent(self):
        self.brief["findings"][1]["certainty"] = 95
        write_record(self.brief, violations_of(self.brief), self.path)
        recorded = load_brief(self.path)
        self.assertEqual(recorded["findings"][1]["certainty"], 80)
        count = len(recorded["findings"])
        write_record(recorded, violations_of(recorded), self.path)
        self.assertEqual(len(load_brief(self.path)["findings"]), count)
        if os.name != "nt":
            self.assertEqual(stat.S_IMODE(self.path.stat().st_mode), 0o600)
        self.assertEqual(list(self.path.parent.glob(".compliance-*")), [])

    def test_linked_brief_cannot_overwrite_another_file(self):
        outside = self.path.parent / "private.yaml"
        outside.write_text("sensitive")
        self.path.unlink()
        try:
            self.path.symlink_to(outside)
        except OSError as exc:
            self.skipTest(f"Symlink creation unavailable: {exc}")
        with self.assertRaises(BriefError):
            write_brief(self.path, self.brief)
        self.assertEqual(outside.read_text(), "sensitive")


if __name__ == "__main__":
    unittest.main()
