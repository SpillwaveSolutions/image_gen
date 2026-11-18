# Image Gen (Spillwave portable edition)

Cover images and in-article illustrations with Nano Banana (Gemini image models) or Grok Imagine.

Built from [SpillwaveSolutions/image_gen](https://github.com/SpillwaveSolutions/image_gen) v2.1.0 and repackaged for Claude Desktop, Cowork, and claude.ai.

## What changed from upstream

- Direct REST backends (`gemini-api`, `xai-api`) using only the Python standard library. A key file is enough; no `imagen` or `grok-img` CLI install.
- Key lookup from env vars or `~/.config/spillwave/image-keys.env`. Keys are never printed.
- `check_setup.py` reports usable backends and blocked hosts.
- Paths resolve from the skill's base directory, so scripts run from any working folder.
- Setup moved from a legacy slash command into the `image-gen-setup` skill.
- The skill now looks at each generated image before delivering it.

## Skills

| Skill | Purpose |
| --- | --- |
| `image-gen` | Plan, generate, check, and place cover and article images |
| `image-gen-setup` | Keys, optional CLIs, network troubleshooting, smoke test |

## Keys

```bash
mkdir -p ~/.config/spillwave
printf 'GEMINI_API_KEY=...\nXAI_API_KEY=...\n' >> ~/.config/spillwave/image-keys.env
chmod 600 ~/.config/spillwave/image-keys.env
```

claude.ai cloud sessions block `generativelanguage.googleapis.com` and `api.x.ai` by default. An org admin can allow them, or run from Claude Desktop/Cowork.

## Backend order (auto)

`imagen` CLI, `gemini-api`, `grok-img` CLI, `xai-api`, `codex`, then fail closed with the prompt saved.

MIT License, Spillwave Solutions.
