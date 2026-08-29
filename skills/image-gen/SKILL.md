---
name: image-gen
description: >
  Generate cover images and in-article illustrations for technical articles.
  Auto image backend: imagen CLI (Nano Banana 2 / Pro), else grok, else codex.
  Triggers: generate images, cover image, article illustrations, visual assets,
  imagen, nano banana, grok imagine.
---

# Image Gen

Article image skill. Not the diagram renderer (that is `imagen-diagrams`).

## When to fire

Use this skill when the user wants a cover image, in-article illustration, or visual assets for an article.

Do not use this skill to render Mermaid or PlantUML. Send those to `imagen-diagrams`.

## Image-engine hint and backend (auto)

Use `--engine-hint imagen`, `--engine-hint grok`, or `--engine-hint codex` when
the caller has a preferred image engine. The hint selects that engine only. It
does not pretend every installed command has a standalone image subcommand.

- **Imagen:** calls the `imagen` CLI directly.
- **Grok:** calls `grok-img`, the noninteractive xAI image CLI. The plugin
  normalizes the generated image to the requested output path.
- **Codex:** starts a Codex agent and asks it to use `image_gen` when that host
  exposes the tool.

Grok and Codex must write the requested PNG. A prose-only Codex result or a
missing grok-img result fails closed and leaves the generated prompt sidecar for
a manual retry. With no hint, `auto` tries each installed engine in order and
falls through after a failed attempt, which lets an unauthenticated Imagen
install reach another configured engine.

1. `imagen` CLI if on PATH. Brace policy: `imagen-cli-vars` (double braces).
2. Then `grok-img` CLI. Brace policy: `grok-imagine` (no rewrite).
3. Else `codex` CLI. Brace policy: `grok-imagine` (no rewrite).
4. Else fail closed. Write `<stem>_imagen.prompt.txt` and exit 2.

Never invent a PNG. If no worker is installed, keep the prompt sidecar and tell the user to run `/image-gen-install`.

## Install the imagen CLI

Latest `gemini-imagen` (`imagen` on PATH) plus Nano Banana model pin:

```bash
python3 skills/image-gen/scripts/install_imagen.py
```

Pins `gemini-3.1-flash-image` (Nano Banana 2) as the CLI default. Cover images use Nano Banana Pro unless the user asks otherwise.

Needs `GOOGLE_API_KEY` or `imagen keys set google YOUR_KEY`.

## Models (Nano Banana, August 2026)

| Alias | Model ID | When |
| --- | --- | --- |
| `nano-banana-2` **(default)** | `gemini-3.1-flash-image` | Article diagrams, high-volume art. 0.5K–4K. |
| `nano-banana-pro` | `gemini-3-pro-image` | Covers, in-image text, dense composition. |
| `nano-banana-2-lite` | `gemini-3.1-flash-lite-image` | Drafts and thumbnails. |
| `nano-banana` | `gemini-2.5-flash-image` | Legacy fallback. |

`--kind cover` selects Pro. `--kind article` selects Nano Banana 2.

## Workflow

### 1. Analyze the article

List 2–4 images (1 cover + 1–3 in-article). One concept per in-article image.

### 2. Generate the cover

Metaphorical, high-impact, 16:9.

```bash
python3 skills/image-gen/scripts/generate.py \
  --kind cover \
  --aspect 16:9 \
  --output work/images/article_cover.png \
  --prompt "A stunning digital art cover image of [metaphor] representing [topic]. Cinematic lighting, professional, high-detail. Style: conceptual 3D render."
```

### 3. Generate in-article images

Direct, labeled, one concept.

```bash
python3 skills/image-gen/scripts/generate.py \
  --kind article \
  --aspect 16:9 \
  --output work/images/article_workflow.png \
  --prompt "A clean technical diagram showing [concept] with color-coded arrows and clear labels. Style: blueprint, professional."

# Ask grok-img to generate with the configured xAI account.
python3 skills/image-gen/scripts/generate.py \
  --kind article \
  --engine-hint grok \
  --aspect 16:9 \
  --output work/images/article_workflow.png \
  --prompt "A clean technical diagram showing [concept]."
```

### 4. Integrate + ALT text

Cover immediately after H1. In-article images at section breaks. ALT text 50–125 characters, specific, no "image" / "diagram" alone.

```markdown
![Architecture diagram showing Cloud Run connecting through a VPC connector to AlloyDB](images/article_cover.png)
```

### 5. Verify

PNG exists. Sidecar `*.json` records backend, policy, model. Prompt sidecar kept next to the PNG.

## Scripts

From `skills/image-gen/scripts/`:

- `generate.py` — write prompt, apply brace policy, call worker, fail closed
- `install_imagen.py` — `pip install -U gemini-imagen` and pin Nano Banana 2
- `backends.py` — PATH detect + brace policy
- `models.py` — Nano Banana catalog

Compatibility: `imagen generate "PROMPT" -o FILE.png` still works if `imagen` is on PATH. Prefer `generate.py` so grok/codex fallback and fail-closed behavior stay intact.

## Prompt craft

Load `references/prompting_guide.md` when the prompt is non-trivial.

Cover: `[Style] cover image of [metaphor] representing [topic], [atmosphere], [composition].`

In-article: `[Style] showing [one concept], [elements], [labels].`

Nano Banana Pro renders in-image text more reliably than Flash. Ask for "clear labels" only when using Pro, or keep labels short.

## Outputs

- `<stem>.png` (or the `--output` path)
- `<stem>_imagen.prompt.txt` (always)
- `<stem>.json` sidecar (backend, policy, model)

If the worker is missing, only the prompt sidecar is written and the process exits 2.
