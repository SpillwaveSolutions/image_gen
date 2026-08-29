#!/usr/bin/env python3
"""Backend detection, brace policy, and argv for image workers."""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path
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
    """Resolve the first installed backend, retained for API compatibility."""
    found = detect_backends(requested)
    return found[0] if found else None


def detect_backends(requested: str = "auto") -> list[ResolvedBackend]:
    """Resolve all installed candidates in preference order.

    Auto mode deliberately returns every usable command. A command existing on
    PATH does not prove that it has credentials, so the renderer can fail over
    when Imagen is installed but not configured.
    """
    requested = (requested or "auto").strip().lower()
    if requested in ("imagen", "imagen-scan"):
        path = shutil.which("imagen")
        if not path:
            return []
        return [ResolvedBackend("imagen", POLICY_FOR[requested], path)]
    if requested in ("grok", "codex"):
        path = shutil.which(requested)
        if not path:
            return []
        return [ResolvedBackend(requested, POLICY_FOR[requested], path)]  # type: ignore[arg-type]
    resolved: list[ResolvedBackend] = []
    for name in AUTO_ORDER:
        path = shutil.which(name)
        if path:
            resolved.append(ResolvedBackend(name, POLICY_FOR[name], path))
    return resolved


def argv_for(
    backend: ResolvedBackend,
    prompt_file: str,
    out_file: str,
    aspect: str,
    model: str | None = None,
) -> list[str]:
    """Build the worker command. Prompt is always also on disk at prompt_file.

    imagen (gemini-imagen): positional/stdin prompt, -o, --aspect-ratio, -m
    grok: Grok Build agent with a prompt file. It uses its native image tool.
    codex: Codex agent running a prompt from stdin. It uses image_gen when
    the host makes that tool available.
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
            "--cwd",
            str(Path(out_file).resolve().parent),
            "--prompt-file",
            prompt_file,
            "--permission-mode",
            "auto",
        ]
        if model:
            cmd.extend(["--model", model])
        return cmd
    cmd: list[str] = [
        backend.binary,
        "exec",
        "--skip-git-repo-check",
        "--ephemeral",
        "--add-dir",
        str(Path(out_file).resolve().parent),
        "-",
    ]
    if model:
        cmd[2:2] = ["--model", model]
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
