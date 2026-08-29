#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/image-gen/scripts"))

from backends import escape_for_backend  # noqa: E402


class BracePolicyTests(unittest.TestCase):
    def test_vars_doubles_braces(self):
        src = "flowchart LR\n  A[Start] --> J{Decision?}\n"
        out = escape_for_backend(src, "imagen-cli-vars")
        self.assertIn("{{Decision?}}", out)
        self.assertNotIn("{Decision?}", out.replace("{{Decision?}}", ""))

    def test_scan_rewrites_to_parens(self):
        src = "flowchart LR\n  A[Start] --> J{Decision?}\n"
        out = escape_for_backend(src, "imagen-cli-scan")
        self.assertIn("(Decision?)", out)
        self.assertNotIn("{Decision?}", out)

    def test_grok_keeps_braces(self):
        src = "flowchart LR\n  A[Start] --> J{Decision?}\n"
        out = escape_for_backend(src, "grok-imagine")
        self.assertIn("{Decision?}", out)
        self.assertNotIn("{{Decision?}}", out)

    def test_article_prompt_with_json_example(self):
        src = 'Cover of an agent writing {"role": "user"} to a file.'
        out = escape_for_backend(src, "imagen-cli-vars")
        self.assertIn('{{"role": "user"}}', out)


if __name__ == "__main__":
    unittest.main()
