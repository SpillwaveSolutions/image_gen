# image-gen

Article cover and in-article image plugin.

- Not the diagram renderer. Mermaid / PlantUML belongs in imagen-diagrams.
- Backend auto: Imagen, then Grok agent, then Codex agent. `--engine-hint`
  explicitly selects one. The agent runners must write the PNG or fail closed.
- Brace policy is per backend. Never copy the wrong escape.
- Install latest `gemini-imagen` with `skills/image-gen/scripts/install_imagen.py`.
- Default model is Nano Banana 2 (`gemini-3.1-flash-image`). Covers use Nano Banana Pro.
- Never invent a PNG.

<!-- worklog:policy:start -->
## WikiTicket SDD (worklog)

Track work with [WikiTicket SDD](https://github.com/SpillwaveSolutions/wiki_ticket_sdd).
Never hand-edit `.work/*.jsonl`.
<!-- worklog:policy:end -->
