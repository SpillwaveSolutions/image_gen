---
name: image-gen-setup
description: Set up or troubleshoot image generation for the image-gen and imagen-diagrams skills, including API keys for Gemini (Nano Banana) and xAI (Grok Imagine), optional CLIs, and blocked network hosts. Use for "set up image gen", "image-gen install", "configure my Gemini key", "why can't you generate images", "imagen not installed".
---

# Image Gen Setup

Get at least one image backend working, then prove it with a check. The image-gen skill's scripts live in the sibling folder `../image-gen/scripts/` relative to this skill's base directory.

```bash
IMG="<base directory for this skill>/../image-gen/scripts"
python3 "$IMG/check_setup.py"
```

## Decide where the skill runs

- **Claude Desktop or Cowork with a folder on the user's computer**: keys live on that computer. Use that machine's shell when one is available.
- **claude.ai cloud session (web, mobile, Projects)**: the sandbox resets and blocks API hosts by default. A key file there does not persist, and `HOST BLOCKED` is expected. Tell the user plainly that generation needs either an org admin to allow `generativelanguage.googleapis.com` and `api.x.ai` in network settings, or a run from Claude Desktop/Cowork. Do not keep retrying.

## Keys (preferred path, no CLI install)

Never ask the user to paste a key into chat, and never write a key the user typed into chat into a file. Have the user create the file themselves. Give them the command for their OS:

macOS / Linux:

```bash
mkdir -p ~/.config/spillwave
printf 'GEMINI_API_KEY=paste-key-here\n' >> ~/.config/spillwave/image-keys.env
chmod 600 ~/.config/spillwave/image-keys.env
```

Windows (PowerShell):

```powershell
New-Item -ItemType Directory -Force "$HOME\.config\spillwave" | Out-Null
Add-Content "$HOME\.config\spillwave\image-keys.env" "GEMINI_API_KEY=paste-key-here"
```

Add `XAI_API_KEY=...` on its own line for Grok Imagine. Keys come from https://aistudio.google.com/apikey (Gemini) and https://console.x.ai (xAI). Environment variables `GEMINI_API_KEY`, `GOOGLE_API_KEY`, and `XAI_API_KEY` also work, as does a file named by `SPILLWAVE_IMAGE_KEYS`.

After the user says the file exists, rerun `check_setup.py`. Success is a `usable:` line that lists `gemini-api` or `xai-api` with no `HOST BLOCKED`.

## Optional CLIs

Only if the user wants them; the REST backends do not need them.

- Imagen CLI: `python3 "$IMG/install_imagen.py"` (installs `gemini-imagen`, pins Nano Banana 2). List models with `--list-models`.
- Grok image CLI (Node 20.19+): `npm install -g grok-image-cli`, then `grok-img auth login`.
- Codex: the user's own install; the adapter asks Codex to write the PNG.

## Smoke test

```bash
python3 "$IMG/generate.py" --kind article --aspect 1:1 \
  --output image-gen-smoke.png --prompt "A small flat icon of a paper airplane, teal on white"
```

Open the PNG to confirm it is a real image, then tell the user setup is done and which backend ran (from `image-gen-smoke.json`).
