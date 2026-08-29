# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## What this is

A multi-host plugin (Claude Code, Codex, Grok Build, Cursor, Agent Plugins 1.0) that generates article cover images and in-article illustrations.

## Commands

```bash
python3 skills/image-gen/scripts/install_imagen.py
python3 skills/image-gen/scripts/generate.py --kind cover --output work/images/cover.png --prompt "PROMPT"
python3 -m unittest discover -s tests -v
```

## Backend auto

1. `imagen` on PATH. Policy `imagen-cli-vars`.
2. Then `grok-img`. Policy `grok-imagine`.
3. Then Codex agent. Policy `grok-imagine`.
4. Else write `<stem>_imagen.prompt.txt` and exit 2.

Use `--engine-hint imagen|grok|codex` to select a runner. `grok` maps to
grok-img. Codex is an agent-host adapter, not an imaginary `image generate`
subcommand. Both must write the requested PNG for a run to pass.

## Models

Pin Nano Banana 2 as the CLI default. `--kind cover` selects Nano Banana Pro (`gemini-3-pro-image`).

## Layout

```
skills/image-gen/     skill + scripts + references
commands/             /image-gen, /image-gen-install
plugin.json           Agent Plugins v1
.claude-plugin/       Claude Code
.codex-plugin/        Codex
.grok-plugin/         Grok Build
.cursor-plugin/       Cursor
```

<!-- worklog:policy:start -->
## WikiTicket SDD (worklog)

Track work with [WikiTicket SDD](https://github.com/SpillwaveSolutions/wiki_ticket_sdd).
Never hand-edit `.work/*.jsonl`.
<!-- worklog:policy:end -->
