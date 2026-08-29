# Image Gen

[![Agent Plugins v1](https://img.shields.io/badge/Agent%20Plugins-v1-0F9D58)](https://agent-plugins.org/specification)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-d97706)](https://code.claude.com/docs/en/plugins)
[![Codex Plugin](https://img.shields.io/badge/Codex-Plugin-10A37F)](https://developers.openai.com/plugins/build/plugins)
[![Grok Build Plugin](https://img.shields.io/badge/Grok%20Build-Plugin-000000)](https://docs.x.ai/build/features/skills-plugins-marketplaces)
[![Skilz Marketplace](https://img.shields.io/badge/Skilz-Marketplace-blue)](https://skillzwave.ai/skill/SpillwaveSolutions__image_gen__image-gen__SKILL/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Cover images and in-article illustrations for technical articles.

Hosts: **Claude Code**, **Codex**, **Grok Build**, **Cursor**, **SKILZ / Agent Plugins 1.0**.

Not the diagram renderer. Mermaid and PlantUML go to [`imagen-diagrams`](https://github.com/SpillwaveSolutions/imagen-diagrams).

## Image-engine hint and backend (auto)

To direct a generation through a specific host, pass one of:

```bash
--engine-hint imagen
--engine-hint grok
--engine-hint codex
```

`imagen` is a direct CLI adapter. `grok` and `codex` are agent adapters: the
plugin sends the art brief to the host and requires it to save a PNG to the
requested output path. If the host returns prose without a file, the command
fails closed and retains the prompt sidecar. With no hint, auto mode tries the
available engines in order and continues after an authentication or runtime
failure.

## Backend order (auto)

1. `imagen` CLI if on PATH. Brace policy: `imagen-cli-vars` (double `{` `}`).
2. Else `grok` CLI. Brace policy: `grok-imagine` (no rewrite).
3. Else `codex` CLI. Brace policy: `grok-imagine` (no rewrite).
4. Else fail closed. Writes `<stem>_imagen.prompt.txt` and exits 2.

## Nano Banana models

The install script upgrades [`gemini-imagen`](https://github.com/aviadr1/gemini-imagen) and pins **Nano Banana 2** (`gemini-3.1-flash-image`). Cover generation uses **Nano Banana Pro** (`gemini-3-pro-image`).

| Alias | Model ID | When |
| --- | --- | --- |
| `nano-banana-2` | `gemini-3.1-flash-image` | Default article art |
| `nano-banana-pro` | `gemini-3-pro-image` | Covers, text-in-image |
| `nano-banana-2-lite` | `gemini-3.1-flash-lite-image` | Drafts |
| `nano-banana` | `gemini-2.5-flash-image` | Legacy fallback |

## Install

### Claude Code / Grok Build

```text
/plugin marketplace add SpillwaveSolutions/image_gen
/plugin install image-gen@spillwave-image-gen
```

Also listed in the skills catalog:

```text
/plugin marketplace add SpillwaveSolutions/skills-marketplace
/plugin install image-gen@spillwave-skills
```

### Codex

```bash
codex plugin marketplace add SpillwaveSolutions/image_gen
```

### Grok Build

```bash
grok plugin install https://github.com/SpillwaveSolutions/image_gen --trust
```

### Skilz

```bash
skilz install SpillwaveSolutions/image_gen
```

### imagen CLI + models

```bash
python3 skills/image-gen/scripts/install_imagen.py
# needs GOOGLE_API_KEY or: imagen keys set google YOUR_KEY
```

## Native plugin manifests

| Host | Manifest | Marketplace |
| --- | --- | --- |
| Claude Code | [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) | [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) |
| Codex | [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json) | [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) |
| Grok Build | [`.grok-plugin/plugin.json`](.grok-plugin/plugin.json) | [`.grok-plugin/marketplace.json`](.grok-plugin/marketplace.json) |
| Cursor | [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json) | [`.cursor/rules/image-gen.mdc`](.cursor/rules/image-gen.mdc) |
| Universal | [`plugin.json`](plugin.json) (Agent Plugins v1) | Skilz |

## Quick start

```bash
mkdir -p work/images

python3 skills/image-gen/scripts/generate.py \
  --kind cover \
  --output work/images/article_cover.png \
  --prompt "A stunning digital art cover image showing three glowing pathways converging into a central AI cloud platform. Dramatic cinematic lighting. Style: conceptual, 3D render, high-detail, professional."

python3 skills/image-gen/scripts/generate.py \
  --kind article \
  --output work/images/article_diagram.png \
  --prompt "Technical diagram showing three color-coded client libraries connecting to a central platform with clear labels. Style: blueprint, clean."
```

Slash commands: `/image-gen`, `/image-gen-install`.

## Commands

```bash
python3 tests/test_backend_detect.py
python3 tests/test_brace_policy.py
python3 tests/test_generate.py
python3 tests/test_models.py
```

## License

MIT.
