#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/image-gen/scripts"))

from backends import (  # noqa: E402
    ResolvedBackend,
    argv_for,
    detect_backend,
    detect_backends,
    grok_img_argv,
    imagen_fallback_argv,
)


class DetectTests(unittest.TestCase):
    def test_auto_prefers_imagen(self):
        def which(name):
            return {"imagen": "/usr/bin/imagen", "grok": "/usr/bin/grok"}.get(name)

        with patch("backends.shutil.which", side_effect=which):
            resolved = detect_backend("auto")
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved.name, "imagen")
        self.assertEqual(resolved.policy, "imagen-cli-vars")

    def test_auto_falls_to_grok(self):
        def which(name):
            return {"grok-img": "/usr/bin/grok-img", "codex": "/usr/bin/codex"}.get(name)

        with patch("backends.shutil.which", side_effect=which):
            resolved = detect_backend("auto")
        self.assertEqual(resolved.name, "grok-img")
        self.assertEqual(resolved.policy, "grok-imagine")

    def test_auto_falls_to_codex(self):
        def which(name):
            return {"codex": "/usr/bin/codex"}.get(name)

        with patch("backends.shutil.which", side_effect=which):
            resolved = detect_backend("auto")
        self.assertEqual(resolved.name, "codex")
        self.assertEqual(resolved.policy, "grok-imagine")

    def test_none_when_missing(self):
        with patch("backends.shutil.which", return_value=None):
            self.assertIsNone(detect_backend("auto"))

    def test_auto_returns_all_candidates_for_runtime_failover(self):
        def which(name):
            return {"imagen": "/usr/bin/imagen", "grok-img": "/usr/bin/grok-img"}.get(name)

        with patch("backends.shutil.which", side_effect=which):
            resolved = detect_backends("auto")
        self.assertEqual([item.name for item in resolved], ["imagen", "grok-img"])

    def test_imagen_argv_uses_prompt_file_and_model(self):
        def which(name):
            return "/usr/bin/imagen" if name == "imagen" else None

        with patch("backends.shutil.which", side_effect=which):
            resolved = detect_backend("imagen")
        cmd = argv_for(resolved, "p.txt", "out.png", "16:9", model="gemini-3.1-flash-image")
        self.assertEqual(cmd[0], "/usr/bin/imagen")
        self.assertIn("--prompt-file", cmd)
        self.assertIn("-o", cmd)
        self.assertIn("--aspect-ratio", cmd)
        self.assertIn("-m", cmd)
        self.assertIn("gemini-3.1-flash-image", cmd)

    def test_imagen_fallback_argv_is_gemini_imagen(self):
        def which(name):
            return "/usr/bin/imagen" if name == "imagen" else None

        with patch("backends.shutil.which", side_effect=which):
            resolved = detect_backend("imagen")
        cmd = imagen_fallback_argv(resolved, "a cat", "out.png", "16:9", model="gemini-3-pro-image")
        self.assertEqual(
            cmd,
            [
                "/usr/bin/imagen",
                "generate",
                "a cat",
                "-o",
                "out.png",
                "--aspect-ratio",
                "16:9",
                "-m",
                "gemini-3-pro-image",
            ],
        )

    def test_grok_img_argv(self):
        def which(name):
            return "/usr/bin/grok-img" if name == "grok-img" else None

        with patch("backends.shutil.which", side_effect=which):
            resolved = detect_backend("grok")
        cmd = grok_img_argv(resolved, "a diagram", "out-dir", "16:9")
        self.assertEqual(
            cmd,
            [
                "/usr/bin/grok-img",
                "generate",
                "a diagram",
                "--aspect-ratio",
                "16:9",
                "--count",
                "1",
                "--output",
                "out-dir",
            ],
        )

    def test_codex_argv_runs_an_agent_not_a_missing_image_subcommand(self):
        backend = ResolvedBackend("codex", "grok-imagine", "/usr/bin/codex")
        cmd = argv_for(backend, "p.txt", "out.png", "16:9")
        self.assertEqual(cmd[0:4], ["/usr/bin/codex", "exec", "--skip-git-repo-check", "--ephemeral"])
        self.assertIn("-", cmd)


if __name__ == "__main__":
    unittest.main()
