# Changelog

## portable 3.0.1

- Codex runs with `-s workspace-write`, so it can save the image. The same fix as 2.1.1 at the repo root.

## portable 3.0.0

- The portable edition for Claude Desktop, Cowork, and claude.ai, built from 2.1.0. It was a claude.ai upload only; it now lives in `portable/`.
- REST backends `gemini-api` and `xai-api` that need only a key file, `check_setup.py`, and the `image-gen-setup` skill.

## 2.1.0

- Add `--engine-hint imagen|grok|codex`.
- Map the Grok hint to grok-img, use an isolated output directory, and
  normalize its generated image to the requested PNG path.
- Run Codex as an agent that uses its native image tool, then verify it wrote
  the requested PNG.
- Auto mode now falls through when an installed engine fails at runtime, such
  as an unconfigured Imagen CLI.

## 2.0.0

- Ship as a Claude Code, Codex, Grok Build, Cursor, and Agent Plugins v1 plugin.
- Auto image backend: `imagen`, then `grok`, then `codex`. Fail closed writes `<stem>_imagen.prompt.txt` and exits 2.
- Brace policies: `imagen-cli-vars`, `imagen-cli-scan`, `grok-imagine`.
- Install script upgrades `gemini-imagen` and pins Nano Banana 2 (`gemini-3.1-flash-image`). Covers use Nano Banana Pro.
- `generate.py` worker replaces ad-hoc `imagen generate` calls so fallback and sidecars stay consistent.

## 1.0.0

- Original Claude Code skill. Direct `imagen generate` against `gemini-2.5-flash-image`.
