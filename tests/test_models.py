#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/image-gen/scripts"))

from models import DEFAULT_MODEL_ID, resolve_model  # noqa: E402


class ModelTests(unittest.TestCase):
    def test_default_is_nano_banana_2(self):
        self.assertEqual(DEFAULT_MODEL_ID, "gemini-3.1-flash-image")
        self.assertEqual(resolve_model(None), "gemini-3.1-flash-image")

    def test_cover_prefers_pro(self):
        self.assertEqual(resolve_model(None, kind="cover"), "gemini-3-pro-image")

    def test_aliases(self):
        self.assertEqual(resolve_model("nano-banana-pro"), "gemini-3-pro-image")
        self.assertEqual(resolve_model("nano-banana-2-lite"), "gemini-3.1-flash-lite-image")
        self.assertEqual(resolve_model("gemini-3.1-flash-image-preview"), "gemini-3.1-flash-image")
        self.assertEqual(resolve_model("gemini-3-pro-image-preview"), "gemini-3-pro-image")
        self.assertEqual(resolve_model("nano-banana"), "gemini-2.5-flash-image")


if __name__ == "__main__":
    unittest.main()
