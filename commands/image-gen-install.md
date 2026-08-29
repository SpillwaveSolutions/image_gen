---
description: Install the latest imagen CLI and pin Nano Banana 2 / Pro models.
---

Run `skills/image-gen/scripts/install_imagen.py`.

1. `pip install -U gemini-imagen` so `imagen` is on PATH.
2. Pin `imagen config set default_model gemini-3.1-flash-image` (Nano Banana 2).
3. Confirm `GOOGLE_API_KEY` or run `imagen keys set google YOUR_KEY`.
4. List models with `python3 skills/image-gen/scripts/install_imagen.py --list-models`.

Cover images still select Nano Banana Pro via `--kind cover` even after the CLI default is Flash.
