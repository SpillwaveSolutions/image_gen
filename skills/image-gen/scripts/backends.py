#!/usr/bin/env python3
"""Backend detection, brace policy, and argv for image workers."""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from typing import Literal

BackendName = Literal["imagen", "grok", "codex"]
BracePolicy = Literal["imagen-cli-vars", "imagen-cli-scan", "grok-imagine"]

POLICY_FOR: dict[str, BracePolicy] = {
    "imagen": "imagen-cli-vars",
    "imagen-scan": "imagen-cli-scan",
    "grok": "grok-imagine",
    "codex": "grok-imagine",
}

AUTO_ORDER: tuple[BackendName, ...] = ("imagen", "grok", "codex")


@dataclass
class ResolvedBackend:
    name: BackendName
    policy: BracePolicy
    binary: str


def escape_for_backend(text: str, policy: BracePolicy) -> str:
    """Apply the brace policy for the chosen image worker.

    imagen-cli-vars     -> double every { and } (gemini-imagen template vars)
    imagen-cli-scan     -> rewrite {token} to (token)
    grok-imagine        -> no brace rewrite
    """
    if policy == "imagen-cli-vars":
        return text.replace("{", "{{").replace("}", "}}")
    if policy == "imagen-cli-scan":
        return re.sub(r"\{([^}]*)\}", r"(\1)", text)
    return text


def detect_backend(requested: str = "auto") -> ResolvedBackend | None:
    requested = (requested or "auto").strip().lower()
    if requested in ("imagen", "imagen-scan"):
        path = shutil.which("imagen")
        if not path:
            return None
        return ResolvedBackend("imagen", POLICY_FOR[requested], path)
    if requested in ("grok", "codex"):
        path = shutil.which(requested)
        if not path:
            return None
        return ResolvedBackend(requested, POLICY_FOR[requested], path)  # type: ignore[arg-type]
    for name in AUTO_ORDER:
        path = shutil.which(name)
        if path:
            return ResolvedBackend(name, POLICY_FOR[name], path)
    return None


def argv_for(
    backend: ResolvedBackend,
    prompt_file: str,
    out_file: str,
    aspect: str,
    model: str | None = None,
) -> list[str]:
    """Build the worker command. Prompt is always also on disk at prompt_file.

    imagen (gemini-imagen): positional/stdin prompt, -o, --aspect-ratio, -m
    grok: grok imagine generate --prompt-file --aspect --output
    codex: codex image generate --prompt-file --aspect --output
    """
    if backend.name == "imagen":
        cmd = [
            backend.binary,
            "generate",
            "--prompt-file",
            prompt_file,
            "--aspect-ratio",
            aspect,
            "-o",
            out_file,
        ]
        if model:
            cmd.extend(["-m", model])
        return cmd
    if backend.name == "grok":
        cmd = [
            backend.binary,
            "imagine",
            "generate",
            "--prompt-file",
            prompt_file,
            "--aspect",
            aspect,
            "--output",
            out_file,
        ]
        if model:
            cmd.extend(["--model", model])
        return cmd
    cmd = [
        backend.binary,
        "image",
        "generate",
        "--prompt-file",
        prompt_file,
        "--aspect",
        aspect,
        "--output",
        out_file,
    ]
    if model:
        cmd.extend(["--model", model])
    return cmd


def imagen_fallback_argv(
    backend: ResolvedBackend,
    prompt: str,
    out_file: str,
    aspect: str,
    model: str | None = None,
) -> list[str]:
    """gemini-imagen 0.6.x has no --prompt-file. Prompt as argv + -o."""
    cmd = [backend.binary, "generate", prompt, "-o", out_file, "--aspect-ratio", aspect]
    if model:
        cmd.extend(["-m", model])
    return cmd
