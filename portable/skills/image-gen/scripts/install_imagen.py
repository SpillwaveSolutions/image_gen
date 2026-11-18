#!/usr/bin/env python3
"""Install or upgrade gemini-imagen (the `imagen` CLI) and pin Nano Banana models."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys

from models import DEFAULT_MODEL_ID, MODELS, PIP_PACKAGE, model_table, resolve_model


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    print(" ".join(cmd))
    return subprocess.run(cmd, check=check, text=True, capture_output=False)


def pip_install() -> int:
    cmd = [sys.executable, "-m", "pip", "install", "-U", PIP_PACKAGE]
    proc = run(cmd, check=False)
    if proc.returncode != 0:
        print(
            f"pip install -U {PIP_PACKAGE} failed ({proc.returncode}). "
            "Try: curl -sSL https://raw.githubusercontent.com/aviadr1/gemini-imagen/main/scripts/install.sh | sh",
            file=sys.stderr,
        )
        return proc.returncode
    return 0


def configure_model(model_id: str) -> int:
    imagen = shutil.which("imagen")
    if not imagen:
        print(
            "imagen is not on PATH after install. Open a new shell, or add the pip scripts dir to PATH.",
            file=sys.stderr,
        )
        return 2
    proc = run([imagen, "config", "set", "default_model", model_id], check=False)
    if proc.returncode != 0:
        print(
            f"Could not pin default_model={model_id}. Set it later with: "
            f"imagen config set default_model {model_id}",
            file=sys.stderr,
        )
        return proc.returncode
    run([imagen, "config", "set", "aspect_ratio", "16:9"], check=False)
    print(f"Pinned imagen default_model={model_id}")
    return 0


def remind_key() -> None:
    if os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY"):
        print("GOOGLE_API_KEY / GEMINI_API_KEY is set.")
        return
    print(
        "No GOOGLE_API_KEY in the environment. After install:\n"
        "  imagen keys set google YOUR_KEY\n"
        "  # or: export GOOGLE_API_KEY=...\n"
        "Get a key at https://aistudio.google.com/apikey"
    )


def main() -> int:
    p = argparse.ArgumentParser(description="Install latest imagen CLI + Nano Banana models")
    p.add_argument(
        "--model",
        default="nano-banana-2",
        help="Alias or model id to pin (default: nano-banana-2)",
    )
    p.add_argument("--skip-install", action="store_true", help="Only configure, do not pip install")
    p.add_argument("--list-models", action="store_true")
    args = p.parse_args()

    if args.list_models:
        print(model_table())
        return 0

    if not args.skip_install:
        code = pip_install()
        if code != 0:
            return code

    model_id = resolve_model(args.model)
    code = configure_model(model_id)
    remind_key()
    print()
    print("Nano Banana models this plugin knows:")
    print(model_table())
    print()
    print(f"Default generation model: {model_id}")
    print(f"Cover images prefer: {MODELS['nano-banana-pro']['id']}")
    print(f"Legacy fallback: {MODELS['nano-banana']['id']}")
    return code


if __name__ == "__main__":
    sys.exit(main())
