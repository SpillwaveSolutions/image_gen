#!/usr/bin/env python3
"""Generate an article image via auto image backend.

Backend order (auto):
1. imagen on PATH. Policy imagen-cli-vars.
2. Else grok on PATH. Policy grok-imagine.
3. Else codex on PATH. Policy grok-imagine.
4. Else fail closed. Write <stem>_imagen.prompt.txt and exit 2.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from backends import (
    argv_for,
    detect_backend,
    escape_for_backend,
    imagen_fallback_argv,
)
from models import DEFAULT_MODEL_ID, resolve_model

SCRIPTS = Path(__file__).resolve().parent


def prompt_path_for(output: Path) -> Path:
    stem = output.stem
    if stem.endswith("_imagen"):
        return output.with_suffix(".prompt.txt")
    return output.with_name(f"{stem}_imagen.prompt.txt")


def png_path_for(output: Path) -> Path:
    if output.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
        return output
    return output.with_suffix(".png")


def imagen_supports_prompt_file(binary: str) -> bool:
    try:
        proc = subprocess.run(
            [binary, "generate", "--help"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return False
    blob = (proc.stdout or "") + (proc.stderr or "")
    return "--prompt-file" in blob


def run_backend(
    resolved,
    prompt: str,
    prompt_file: Path,
    out: Path,
    aspect: str,
    model: str | None,
    dry_run: bool,
) -> int:
    if resolved.name == "imagen" and not imagen_supports_prompt_file(resolved.binary):
        cmd = imagen_fallback_argv(
            resolved, prompt, str(out), aspect, model=model
        )
    else:
        cmd = argv_for(
            resolved, str(prompt_file), str(out), aspect, model=model
        )
    print(" ".join(cmd if resolved.name != "imagen" else _redact_prompt(cmd)))
    if dry_run:
        return 0
    try:
        proc = subprocess.run(cmd, check=False)
    except FileNotFoundError:
        print(f"backend binary missing: {resolved.binary}", file=sys.stderr)
        return 2
    return proc.returncode


def _redact_prompt(cmd: list[str]) -> list[str]:
    """Do not echo a multi-hundred-word prompt on the console."""
    out = list(cmd)
    if len(out) >= 3 and out[1] == "generate" and not out[2].startswith("-"):
        out[2] = "<prompt>"
    return out


def main() -> int:
    p = argparse.ArgumentParser(description="image-gen article image renderer")
    p.add_argument("--prompt", help="Image prompt text")
    p.add_argument("--prompt-file", help="Read prompt from this file")
    p.add_argument("--output", required=True, help="Output PNG path")
    p.add_argument("--kind", choices=("cover", "article", "default"), default="default")
    p.add_argument("--aspect", default="16:9")
    p.add_argument("--backend", default="auto")
    p.add_argument("--model", help="Model id or alias (nano-banana-2, nano-banana-pro, ...)")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    if args.prompt_file:
        prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    elif args.prompt:
        prompt = args.prompt
    elif not sys.stdin.isatty():
        prompt = sys.stdin.read()
    else:
        print("Provide --prompt, --prompt-file, or stdin.", file=sys.stderr)
        return 2

    out = png_path_for(Path(args.output))
    out.parent.mkdir(parents=True, exist_ok=True)
    sidecar = out.with_suffix(".json")
    prompt_file = prompt_path_for(out)

    resolved = detect_backend(args.backend)
    policy = resolved.policy if resolved else "imagen-cli-vars"
    escaped = escape_for_backend(prompt, policy)
    prompt_file.write_text(escaped, encoding="utf-8")

    model = resolve_model(args.model, kind=args.kind) if resolved and resolved.name == "imagen" else args.model
    if resolved and resolved.name == "imagen" and not model:
        model = DEFAULT_MODEL_ID

    sidecar_data = {
        "png": str(out),
        "prompt": str(prompt_file),
        "kind": args.kind,
        "aspect": args.aspect,
        "backend": resolved.name if resolved else None,
        "policy": policy,
        "model": model,
    }
    sidecar.write_text(json.dumps(sidecar_data, indent=2) + "\n", encoding="utf-8")

    if not resolved:
        print(
            "No image backend on PATH (imagen, grok, or codex). "
            f"Wrote prompt to {prompt_file}.",
            file=sys.stderr,
        )
        return 2

    code = run_backend(
        resolved,
        escaped,
        prompt_file,
        out,
        args.aspect,
        model,
        args.dry_run,
    )
    if code != 0:
        print(
            f"backend exited {code}. Prompt kept at {prompt_file}.",
            file=sys.stderr,
        )
        return code if code != 0 else 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
