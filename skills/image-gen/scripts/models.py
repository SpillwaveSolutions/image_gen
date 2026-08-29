#!/usr/bin/env python3
"""Nano Banana / Gemini image model catalog (August 2026)."""

from __future__ import annotations

# Latest Nano Banana family. Default is Nano Banana 2.
# Preview IDs are aliases the Gemini API still accepts.
MODELS: dict[str, dict[str, str]] = {
    "nano-banana-2": {
        "id": "gemini-3.1-flash-image",
        "alias": "gemini-3.1-flash-image-preview",
        "label": "Nano Banana 2 (Gemini 3.1 Flash Image)",
        "use": "Default. Covers, diagrams, high-volume article art. 0.5K-4K.",
    },
    "nano-banana-2-lite": {
        "id": "gemini-3.1-flash-lite-image",
        "alias": "gemini-3.1-flash-lite-image",
        "label": "Nano Banana 2 Lite (Gemini 3.1 Flash Lite Image)",
        "use": "Cheapest/fastest. Thumbnails and drafts. Not for multi-ref edits.",
    },
    "nano-banana-pro": {
        "id": "gemini-3-pro-image",
        "alias": "gemini-3-pro-image-preview",
        "label": "Nano Banana Pro (Gemini 3 Pro Image)",
        "use": "Studio covers, in-image text, dense diagrams, final polish. 1K-4K.",
    },
    "nano-banana": {
        "id": "gemini-2.5-flash-image",
        "alias": "gemini-2.5-flash-image",
        "label": "Nano Banana (Gemini 2.5 Flash Image, legacy)",
        "use": "Fallback if a 3.x image model is unavailable.",
    },
}

DEFAULT_KIND_MODEL = {
    "cover": "nano-banana-pro",
    "article": "nano-banana-2",
    "default": "nano-banana-2",
}

DEFAULT_MODEL_ID = MODELS["nano-banana-2"]["id"]
PIP_PACKAGE = "gemini-imagen"


def resolve_model(name: str | None, kind: str = "default") -> str:
    if not name:
        key = DEFAULT_KIND_MODEL.get(kind, DEFAULT_KIND_MODEL["default"])
        return MODELS[key]["id"]
    raw = name.strip().lower()
    if raw in MODELS:
        return MODELS[raw]["id"]
    for spec in MODELS.values():
        if raw in (spec["id"].lower(), spec["alias"].lower()):
            return spec["id"]
    return name.strip()


def model_table() -> str:
    lines = ["| Alias | Model ID | When |", "| --- | --- | --- |"]
    for key, spec in MODELS.items():
        default = " **(default)**" if key == "nano-banana-2" else ""
        lines.append(f"| `{key}`{default} | `{spec['id']}` | {spec['use']} |")
    return "\n".join(lines)
