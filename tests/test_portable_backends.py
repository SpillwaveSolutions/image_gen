#!/usr/bin/env python3
"""The portable edition (portable/) builds the same codex command as the root plugin."""
import importlib.util
import sys
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "portable/skills/image-gen/scripts/backends.py"
# A unique module name, so this test never shares a module with the root backends.py.
spec = importlib.util.spec_from_file_location("portable_backends", PATH)
portable = importlib.util.module_from_spec(spec)
sys.modules["portable_backends"] = portable  # dataclass needs its module registered
spec.loader.exec_module(portable)


class PortableCodexTests(unittest.TestCase):
    def test_codex_argv_can_write_the_output(self):
        backend = portable.ResolvedBackend("codex", "grok-imagine", "/usr/bin/codex")
        cmd = portable.argv_for(backend, "p.txt", "out.png", "16:9")
        self.assertEqual(cmd[0:4], ["/usr/bin/codex", "exec", "--skip-git-repo-check", "--ephemeral"])
        self.assertEqual(cmd[cmd.index("-s") + 1], "workspace-write")
        self.assertEqual(cmd[-1], "-")


if __name__ == "__main__":
    unittest.main()
