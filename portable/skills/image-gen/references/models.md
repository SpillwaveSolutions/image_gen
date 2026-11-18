# Nano Banana models (August 2026)

Google image generation on Gemini is branded Nano Banana. Imagen 4.x models are shut down. Use Gemini 3.x Image IDs.

| Nickname | API model ID | Alias still accepted | Role |
| --- | --- | --- | --- |
| Nano Banana 2 | `gemini-3.1-flash-image` | `gemini-3.1-flash-image-preview` | Default. Fast, 0.5K–4K. |
| Nano Banana 2 Lite | `gemini-3.1-flash-lite-image` | same | Cheapest. Drafts. |
| Nano Banana Pro | `gemini-3-pro-image` | `gemini-3-pro-image-preview` | Covers, text-in-image, polish. |
| Nano Banana (legacy) | `gemini-2.5-flash-image` | same | Fallback only. |

This plugin pins the `imagen` CLI default to Nano Banana 2:

```bash
python3 skills/image-gen/scripts/install_imagen.py
imagen config set default_model gemini-3.1-flash-image
```

Cover generation (`--kind cover`) uses Nano Banana Pro. Override with `--model nano-banana-2` or a raw ID.

Docs: [Gemini image generation](https://ai.google.dev/gemini-api/docs/image-generation).
