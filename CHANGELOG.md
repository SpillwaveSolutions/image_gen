# Changelog

## 2.0.0

- Ship as a Claude Code, Codex, Grok Build, Cursor, and Agent Plugins v1 plugin.
- Auto image backend: `imagen`, then `grok`, then `codex`. Fail closed writes `<stem>_imagen.prompt.txt` and exits 2.
- Brace policies: `imagen-cli-vars`, `imagen-cli-scan`, `grok-imagine`.
- Install script upgrades `gemini-imagen` and pins Nano Banana 2 (`gemini-3.1-flash-image`). Covers use Nano Banana Pro.
- `generate.py` worker replaces ad-hoc `imagen generate` calls so fallback and sidecars stay consistent.

## 1.0.0

- Original Claude Code skill. Direct `imagen generate` against `gemini-2.5-flash-image`.
