---
description: Generate a cover or in-article image via imagen, grok, or codex.
---

Run `skills/image-gen/scripts/generate.py`.

1. Choose kind: cover (Nano Banana Pro, 16:9) or article (Nano Banana 2).
2. Write a specific prompt. Covers are metaphorical. In-article images explain one concept.
3. Call generate.py with `--output` under `work/images/`.
4. Use `--engine-hint imagen|grok|codex` when the host matters. Grok and Codex
   are agent runners and must write the requested PNG; prose-only results fail
   closed with a retained prompt sidecar.
5. If exit 2, no backend is on PATH. The prompt sidecar is already written. Run `/image-gen-install` or install grok/codex.
6. Integrate the PNG with 50–125 character ALT text.

Do not invent a PNG. Do not send Mermaid or PlantUML through this command.
