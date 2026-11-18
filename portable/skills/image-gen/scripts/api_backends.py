#!/usr/bin/env python3
"""Direct REST image backends. No CLI install needed.

gemini-api : Google Gemini image models (Nano Banana family) via generateContent.
xai-api    : xAI Grok Imagine via /v1/images/generations.

Both use only the Python standard library, so they work in Claude Desktop,
Cowork, Claude Code, and claude.ai code execution, as long as the host can
reach the API domain. Keys never print.

Key resolution order (first hit wins):
  1. Environment: GEMINI_API_KEY or GOOGLE_API_KEY, XAI_API_KEY
  2. File named by SPILLWAVE_IMAGE_KEYS
  3. ~/.config/spillwave/image-keys.env
  4. ./.image-keys.env, then ./.env (current working directory)
Files use KEY=VALUE lines. Lines starting with # are ignored.
"""

from __future__ import annotations

import base64
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from io import BytesIO
from pathlib import Path

GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
XAI_ENDPOINT = "https://api.x.ai/v1/images/generations"
XAI_DEFAULT_MODEL = "grok-imagine-image"

GOOGLE_KEY_NAMES = ("GEMINI_API_KEY", "GOOGLE_API_KEY")
XAI_KEY_NAMES = ("XAI_API_KEY",)

NETWORK_HINT = (
    "This environment cannot reach {host}. In a claude.ai cloud session the "
    "workspace only allows package registries and GitHub by default; an org "
    "admin can allow {host} under Admin settings > Capabilities. Otherwise run "
    "the skill from Claude Desktop or Cowork with a folder on your own computer."
)


class BackendUnavailable(RuntimeError):
    """Raised when a backend cannot run here (no key, no network)."""


def _key_files() -> list[Path]:
    files: list[Path] = []
    explicit = os.environ.get("SPILLWAVE_IMAGE_KEYS")
    if explicit:
        files.append(Path(explicit).expanduser())
    files.append(Path.home() / ".config" / "spillwave" / "image-keys.env")
    files.append(Path.cwd() / ".image-keys.env")
    files.append(Path.cwd() / ".env")
    return files


def _read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return values
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export ") :]
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def resolve_key(names: tuple[str, ...]) -> tuple[str | None, str | None]:
    """Return (key, where_found). where_found never contains the key."""
    for name in names:
        value = os.environ.get(name)
        if value:
            return value, f"env:{name}"
    for path in _key_files():
        if not path.is_file():
            continue
        values = _read_env_file(path)
        for name in names:
            if values.get(name):
                return values[name], f"file:{path}"
    return None, None


def google_key() -> tuple[str | None, str | None]:
    return resolve_key(GOOGLE_KEY_NAMES)


def xai_key() -> tuple[str | None, str | None]:
    return resolve_key(XAI_KEY_NAMES)


def _ssl_context() -> ssl.SSLContext:
    bundle = (
        os.environ.get("SSL_CERT_FILE")
        or os.environ.get("REQUESTS_CA_BUNDLE")
        or os.environ.get("CURL_CA_BUNDLE")
    )
    if bundle and Path(bundle).is_file():
        return ssl.create_default_context(cafile=bundle)
    return ssl.create_default_context()


def _post_json(url: str, body: dict, headers: dict[str, str], timeout: int = 180) -> dict:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    for k, v in headers.items():
        req.add_header(k, v)
    host = urllib.request.urlparse(url).hostname or url
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ssl_context()) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", errors="replace")[:1200]
        raise urllib.error.HTTPError(err.url, err.code, detail, err.headers, None) from None
    except (urllib.error.URLError, OSError) as err:
        raise BackendUnavailable(f"{NETWORK_HINT.format(host=host)} ({err})") from None


def _write_image(raw: bytes, mime: str, out: Path) -> None:
    """Write bytes to out, converting format when the extension disagrees."""
    want = out.suffix.lower().lstrip(".") or "png"
    want = "jpeg" if want == "jpg" else want
    have = (mime.split("/")[-1] or "png").lower()
    have = "jpeg" if have == "jpg" else have
    out.parent.mkdir(parents=True, exist_ok=True)
    if have == want:
        out.write_bytes(raw)
        return
    try:
        from PIL import Image  # type: ignore

        img = Image.open(BytesIO(raw))
        if want == "jpeg" and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(out, format=want.upper())
    except Exception:  # Pillow missing or conversion failed: keep real bytes
        out.write_bytes(raw)
        print(
            f"note: API returned {mime}; saved without conversion to {out}",
            file=sys.stderr,
        )


def gemini_generate(
    prompt: str,
    out: Path,
    aspect: str,
    model_ids: list[str],
    image_size: str | None = None,
) -> str:
    """Generate one image with Gemini. Tries each model id in order. Returns model used."""
    key, _ = google_key()
    if not key:
        raise BackendUnavailable("No GEMINI_API_KEY / GOOGLE_API_KEY found.")
    image_config: dict[str, str] = {"aspectRatio": aspect}
    if image_size:
        image_config["imageSize"] = image_size
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"],
            "imageConfig": image_config,
        },
    }
    last_error = "no model tried"
    for model in model_ids:
        try:
            data = _post_json(
                GEMINI_ENDPOINT.format(model=model), body, {"x-goog-api-key": key}
            )
        except urllib.error.HTTPError as err:
            last_error = f"{model}: HTTP {err.code} {err.msg}"
            if err.code in (400, 404):
                continue  # unknown model id or unsupported config; try the next id
            raise RuntimeError(last_error) from None
        texts: list[str] = []
        for cand in data.get("candidates", []):
            for part in (cand.get("content") or {}).get("parts", []):
                inline = part.get("inlineData") or part.get("inline_data")
                if inline and inline.get("data"):
                    _write_image(
                        base64.b64decode(inline["data"]),
                        inline.get("mimeType") or inline.get("mime_type") or "image/png",
                        out,
                    )
                    return model
                if part.get("text"):
                    texts.append(part["text"])
        reason = data.get("promptFeedback") or (data.get("candidates") or [{}])[0].get("finishReason")
        last_error = f"{model}: no image in response ({reason}) {' '.join(texts)[:300]}"
    raise RuntimeError(last_error)


def xai_generate(prompt: str, out: Path, aspect: str, model: str | None = None) -> str:
    key, _ = xai_key()
    if not key:
        raise BackendUnavailable("No XAI_API_KEY found.")
    model = model or XAI_DEFAULT_MODEL
    body = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "response_format": "b64_json",
        "aspect_ratio": aspect,
    }
    headers = {"Authorization": f"Bearer {key}"}
    try:
        data = _post_json(XAI_ENDPOINT, body, headers)
    except urllib.error.HTTPError as err:
        if err.code != 400:
            raise RuntimeError(f"xai {model}: HTTP {err.code} {err.msg}") from None
        body.pop("aspect_ratio", None)  # older API revisions reject the field
        try:
            data = _post_json(XAI_ENDPOINT, body, headers)
        except urllib.error.HTTPError as err2:
            raise RuntimeError(f"xai {model}: HTTP {err2.code} {err2.msg}") from None
    items = data.get("data") or []
    if not items:
        raise RuntimeError(f"xai {model}: empty response")
    item = items[0]
    if item.get("b64_json"):
        _write_image(base64.b64decode(item["b64_json"]), "image/jpeg", out)
        return model
    if item.get("url"):
        req = urllib.request.Request(item["url"])
        try:
            with urllib.request.urlopen(req, timeout=120, context=_ssl_context()) as resp:
                _write_image(resp.read(), resp.headers.get_content_type(), out)
        except (urllib.error.URLError, OSError) as err:
            raise BackendUnavailable(f"could not download xai image url ({err})") from None
        return model
    raise RuntimeError(f"xai {model}: no image payload")


def key_status() -> dict[str, str]:
    """Human-safe report of which keys are configured and where."""
    _, g = google_key()
    _, x = xai_key()
    return {"google": g or "missing", "xai": x or "missing"}


if __name__ == "__main__":
    print(json.dumps(key_status(), indent=2))
