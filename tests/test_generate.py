#!/usr/bin/env python3
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/image-gen/scripts"))

import generate  # noqa: E402
from backends import ResolvedBackend  # noqa: E402


class GenerateTests(unittest.TestCase):
    def test_prompt_path_adds_imagen_suffix(self):
        self.assertEqual(
            generate.prompt_path_for(Path("work/images/cover.png")),
            Path("work/images/cover_imagen.prompt.txt"),
        )
        self.assertEqual(
            generate.prompt_path_for(Path("work/images/cover_imagen.png")),
            Path("work/images/cover_imagen.prompt.txt"),
        )

    def test_fail_closed_writes_prompt_and_exits_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "cover.png"
            argv = [
                "generate.py",
                "--prompt",
                "A dramatic 3D render of {Decision?} in a dark room.",
                "--output",
                str(out),
            ]
            with patch.object(sys, "argv", argv), patch(
                "generate.detect_backend", return_value=None
            ):
                code = generate.main()
            self.assertEqual(code, 2)
            prompt = Path(tmp) / "cover_imagen.prompt.txt"
            self.assertTrue(prompt.exists())
            text = prompt.read_text(encoding="utf-8")
            self.assertIn("{{Decision?}}", text)
            sidecar = Path(tmp) / "cover.json"
            data = json.loads(sidecar.read_text(encoding="utf-8"))
            self.assertIsNone(data["backend"])
            self.assertEqual(data["policy"], "imagen-cli-vars")

    def test_dry_run_imagen_uses_fallback_without_prompt_file_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "diagram.png"
            argv = [
                "generate.py",
                "--prompt",
                "technical diagram",
                "--output",
                str(out),
                "--dry-run",
            ]
            backend = ResolvedBackend("imagen", "imagen-cli-vars", "/usr/bin/imagen")
            with patch.object(sys, "argv", argv), patch(
                "generate.detect_backend", return_value=backend
            ), patch("generate.imagen_supports_prompt_file", return_value=False), patch(
                "generate.subprocess.run"
            ) as run:
                code = generate.main()
            self.assertEqual(code, 0)
            run.assert_not_called()  # dry-run prints but does not execute
            self.assertTrue((Path(tmp) / "diagram_imagen.prompt.txt").exists())


if __name__ == "__main__":
    unittest.main()
