---
name: image-gen
description: Generate cover images and in-article illustrations for articles, posts, decks, and docs with Nano Banana (Gemini image models) or Grok Imagine. Use for "generate an image", "make a cover image", "hero image for this article", "illustrate this section", "visual assets", "nano banana", "imagen", "grok imagine". Not for rendering Mermaid or PlantUML source; send those to imagen-diagrams or plantuml.
---

# Image Gen

Article image skill. Not the diagram renderer (that is `imagen-diagrams`).

## Paths

All scripts live in `scripts/` inside this skill's base directory (shown as "Base directory for this skill" when the skill loads). In every command below, set `SKILL` to that directory first:

```bash
SKILL="<base directory for this skill>"
```

Write images into the user's project folder when one is connected (for example `images/` next to the article). Otherwise write into the working directory and hand the final PNG to the user with the file-sending tool.

## Step 0: Check what can run here

```bash
python3 "$SKILL/scripts/check_setup.py"
```

The report lists each backend and ends with `usable:`. If `usable: none`, do not try to generate. Write the prompt anyway (step 2 does this automatically) and tell the user in one or two sentences what is missing, using the report's own advice. The usual fixes:

- Add `GEMINI_API_KEY=...` (and optionally `XAI_API_KEY=...`) to `~/.config/spillwave/image-keys.env` on the machine that runs the skill. Load the `image-gen-setup` skill to walk the user through it.
- `HOST BLOCKED` in a claude.ai cloud session means the sandbox network does not allow the API domain. An org admin can allow `generativelanguage.googleapis.com` and `api.x.ai`, or the user can run the skill from Claude Desktop or Cowork against a folder on their own computer.

Never ask the user to paste an API key into chat. Never print, echo, or log a key.

## Backends (auto order)

1. `imagen` CLI on PATH (gemini-imagen). Brace policy `imagen-cli-vars`.
2. `gemini-api`: direct REST call when a Google key is configured. No CLI needed. No brace rewrite.
3. `grok-img` CLI on PATH. No brace rewrite.
4. `xai-api`: direct REST call when an xAI key is configured. No brace rewrite.
5. `codex` CLI on PATH (agent adapter; must write the PNG).
6. None: fail closed. Write `<stem>_imagen.prompt.txt`, exit 2.

Auto mode tries each usable backend and falls through on failure. `--engine-hint imagen` means Google (CLI then REST), `--engine-hint grok` means xAI (CLI then REST), plus `gemini`, `xai`, `codex` for a single backend. Exit codes: 0 ok, 2 no backend, 4 worker produced no image, 5 network blocked.

Never invent a PNG. Never draw a substitute with code and call it the generated image.

## Models (Nano Banana)

| Alias | Model ID | When |
| --- | --- | --- |
| `nano-banana-2` (default) | `gemini-3.1-flash-image` | In-article art, high volume |
| `nano-banana-pro` | `gemini-3-pro-image` | Covers, in-image text, dense composition |
| `nano-banana-2-lite` | `gemini-3.1-flash-lite-image` | Drafts, thumbnails |
| `nano-banana` | `gemini-2.5-flash-image` | Legacy fallback |

`--kind cover` selects Pro. `--kind article` selects Nano Banana 2. The REST backend retries the preview alias, then the legacy model, when an id is rejected. Details: `references/models.md`.

## Workflow

### 1. Analyze the article

Read the article or brief. Plan 2 to 4 images: 1 cover and 1 to 3 in-article images, one concept each. If the user asked for one image, make one.

### 2. Generate the cover

Metaphorical, high impact, 16:9.

```bash
python3 "$SKILL/scripts/generate.py" \
  --kind cover --aspect 16:9 \
  --output images/article_cover.png \
  --prompt "A stunning digital art cover image of [metaphor] representing [topic]. Cinematic lighting, professional, high detail. Style: conceptual 3D render."
```

### 3. Generate in-article images

Direct, labeled, one concept.

```bash
python3 "$SKILL/scripts/generate.py" \
  --kind article --aspect 16:9 \
  --output images/article_workflow.png \
  --prompt "A clean technical illustration showing [concept] with color-coded arrows and short clear labels. Style: blueprint, professional."
```

Add `--engine-hint grok` to prefer Grok Imagine. Use `--prompt-file` for long prompts. Add `--dry-run` to see the chosen backend without spending a call.

### 4. Look at the result

Open each PNG with the file-reading tool and check it: subject matches the brief, labels are spelled correctly, no garbled text, no watermark. If a label is wrong, regenerate once with the label text quoted exactly in the prompt, or ask for fewer labels. Report a remaining flaw honestly instead of hiding it.

### 5. Integrate and write ALT text

Cover goes right after the H1. In-article images go at section breaks. ALT text is 50 to 125 characters, specific, never just "image" or "diagram".

```markdown
![Cloud Run service connecting through a VPC connector to AlloyDB](images/article_workflow.png)
```

### 6. Deliver

Confirm the PNG exists and the `.json` sidecar names the backend and model. Send the image file(s) to the user. Keep the `_imagen.prompt.txt` sidecar next to each image for reruns.

## Prompt craft

Load `references/prompting_guide.md` when the prompt is non-trivial.

- Cover: `[Style] cover image of [metaphor] representing [topic], [atmosphere], [composition].`
- In-article: `[Style] showing [one concept], [elements], [labels].`

Nano Banana Pro renders in-image text more reliably than Flash. Ask for labels only with Pro, or keep labels to a few short words.

## Scripts

- `generate.py`: write the prompt, apply brace policy per backend, call the worker, fall through, fail closed
- `check_setup.py`: report usable backends, key location (never the key), host reachability
- `api_backends.py`: stdlib REST clients for Gemini and xAI, key resolution
- `backends.py`: backend detection and brace policy
- `models.py`: Nano Banana catalog
- `install_imagen.py`: optional `pip install -U gemini-imagen` and model pin

## Outputs

- `<stem>.png` (or the `--output` path)
- `<stem>_imagen.prompt.txt` (always)
- `<stem>.json` sidecar (backend, policy, model, attempts)
