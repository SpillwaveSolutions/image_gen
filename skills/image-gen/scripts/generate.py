#!/usr/bin/env python3
"""Generate an article image via auto image backend.

Backend order (auto):
1. imagen on PATH. Policy imagen-cli-vars.
2. Then grok-img on PATH. Policy grok-imagine.
3. Else codex on PATH. Policy grok-imagine.
4. Else fail closed. Write <stem>_imagen.prompt.txt and exit 2.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from backends import (
    argv_for,
    detect_backends,
    escape_for_backend,
    grok_img_argv,
    imagen_fallback_argv,
)
from models import DEFAULT_MODEL_ID, resolve_model

SCRIPTS = Path(__file__).resolve().parent
GROK_IMG_DEFAULT_MODEL = "grok-imagine-image"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


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
    if resolved.name == "grok-img":
        stage = Path(tempfile.mkdtemp(prefix=f".{out.stem}.grok-img-", dir=out.parent))
        try:
            cmd = grok_img_argv(resolved, prompt, str(stage), aspect, model=model)
            print(" ".join(_redact_prompt(cmd)))
            if dry_run:
                return 0
            proc = subprocess.run(cmd, check=False)
            if proc.returncode != 0:
                return proc.returncode
            generated = sorted(
                (path for path in stage.rglob("*") if path.suffix.lower() in IMAGE_EXTENSIONS),
                key=lambda path: path.stat().st_mtime,
                reverse=True,
            )
            if not generated:
                print("grok-img exited without writing an image.", file=sys.stderr)
                return 4
            shutil.copy2(generated[0], out)
            return 0
        finally:
            shutil.rmtree(stage, ignore_errors=True)

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
        agent_host = resolved.name == "codex"
        proc = subprocess.run(
            cmd,
            check=False,
            input=prompt if resolved.name == "codex" else None,
            text=agent_host,
            capture_output=agent_host,
        )
    except FileNotFoundError:
        print(f"backend binary missing: {resolved.binary}", file=sys.stderr)
        return 2
    if proc.returncode != 0:
        if agent_host:
            diagnostics = ((proc.stdout or "") + (proc.stderr or "")).strip()
            if diagnostics:
                print(diagnostics[-2000:], file=sys.stderr)
        return proc.returncode
    if resolved.name == "codex" and not out.exists():
        print(
            f"{resolved.name} exited without writing {out}. "
            "Prompt kept for manual retry.",
            file=sys.stderr,
        )
        return 4
    return 0


def _redact_prompt(cmd: list[str]) -> list[str]:
    """Do not echo a multi-hundred-word prompt on the console."""
    out = list(cmd)
    if len(out) >= 3 and out[1] == "generate" and not out[2].startswith("-"):
        out[2] = "<prompt>"
    return out


def agent_prompt(engine: str, prompt: str, out: Path, aspect: str) -> str:
    """Ask an agent host to create a file, instead of pretending it has a CLI subcommand."""
    return "\n\n".join(
        [
            f"Use your native {engine} image-generation capability to create one final PNG.",
            f"Save the PNG exactly at: {out}",
            f"Aspect ratio: {aspect}. Do not return prose only. Do not change the path.",
            "Image brief:",
            prompt,
        ]
    )


def main() -> int:
    p = argparse.ArgumentParser(description="image-gen article image renderer")
    p.add_argument("--prompt", help="Image prompt text")
    p.add_argument("--prompt-file", help="Read prompt from this file")
    p.add_argument("--output", required=True, help="Output PNG path")
    p.add_argument("--kind", choices=("cover", "article", "default"), default="default")
    p.add_argument("--aspect", default="16:9")
    p.add_argument("--backend", default="auto")
    p.add_argument(
        "--engine-hint",
        choices=("auto", "imagen", "grok", "codex"),
        default="auto",
        help="Prefer this image engine. In auto mode, failed workers fall through to the next installed engine.",
    )
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

    if args.backend != "auto" and args.engine_hint != "auto":
        p.error("Use either --backend or --engine-hint, not both.")
    requested = args.engine_hint if args.engine_hint != "auto" else args.backend
    resolved_backends = detect_backends(requested)
    sidecar_data = {
        "png": str(out),
        "prompt": str(prompt_file),
        "kind": args.kind,
        "aspect": args.aspect,
        "engine_hint": args.engine_hint,
        "backend": None,
        "policy": "imagen-cli-vars",
        "model": args.model,
        "attempts": [],
    }

    if not resolved_backends:
        prompt_file.write_text(
            escape_for_backend(prompt, "imagen-cli-vars"), encoding="utf-8"
        )
        sidecar.write_text(json.dumps(sidecar_data, indent=2) + "\n", encoding="utf-8")
        print(
            "No image backend on PATH (imagen, grok-img, or codex). "
            f"Wrote prompt to {prompt_file}.",
            file=sys.stderr,
        )
        return 2

    last_code = 2
    for resolved in resolved_backends:
        policy = resolved.policy
        worker_prompt = (
            prompt
            if resolved.name != "codex"
            else agent_prompt(resolved.name, prompt, out, args.aspect)
        )
        escaped = escape_for_backend(worker_prompt, policy)
        prompt_file.write_text(escaped, encoding="utf-8")
        model = (
            resolve_model(args.model, kind=args.kind)
            if resolved.name == "imagen"
            else args.model
        )
        if resolved.name == "imagen" and not model:
            model = DEFAULT_MODEL_ID
        if resolved.name == "grok-img" and not model:
            model = GROK_IMG_DEFAULT_MODEL
        code = run_backend(
            resolved,
            escaped,
            prompt_file,
            out,
            args.aspect,
            model,
            args.dry_run,
        )
        sidecar_data.update(
            {
                "backend": resolved.name,
                "policy": policy,
                "model": model,
            }
        )
        sidecar_data["attempts"].append({"backend": resolved.name, "exit_code": code})
        sidecar.write_text(json.dumps(sidecar_data, indent=2) + "\n", encoding="utf-8")
        if code == 0:
            return 0
        last_code = code
        if requested != "auto":
            break
    print(f"all image backends failed. Prompt kept at {prompt_file}.", file=sys.stderr)
    return last_code


if __name__ == "__main__":
    sys.exit(main())
