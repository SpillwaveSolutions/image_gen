# Backends and brace policy

## Auto order

1. `imagen` if on PATH. Policy `imagen-cli-vars`.
2. `gemini-api` if a Google key resolves. REST, stdlib only. Policy `grok-imagine`.
3. `grok-img` if on PATH. Policy `grok-imagine`.
4. `xai-api` if an xAI key resolves. REST, stdlib only. Policy `grok-imagine`.
5. `codex` if on PATH. Policy `grok-imagine`.
6. Else fail closed. Write `<stem>_imagen.prompt.txt` and exit 2.

Pin with `--backend imagen|imagen-scan|gemini-api|grok-img|xai-api|codex|auto`,
or prefer an engine family with `--engine-hint imagen|gemini|grok|xai|codex`.
`imagen` covers the CLI then REST; `grok` covers grok-img then REST.

Key lookup for REST: env `GEMINI_API_KEY`/`GOOGLE_API_KEY`/`XAI_API_KEY`, then
the file named by `SPILLWAVE_IMAGE_KEYS`, then `~/.config/spillwave/image-keys.env`,
then `./.image-keys.env` and `./.env`.

REST endpoints:

```text
POST https://generativelanguage.googleapis.com/v1beta/models/MODEL:generateContent
     header x-goog-api-key, generationConfig.responseModalities [IMAGE, TEXT],
     generationConfig.imageConfig.aspectRatio
POST https://api.x.ai/v1/images/generations
     Authorization: Bearer, model grok-imagine-image, response_format b64_json
```

## Policies

```text
imagen-cli-vars     -> double every { and }
imagen-cli-scan     -> rewrite {token} to (token)
grok-imagine        -> no brace rewrite
```

A `{Decision?}` node or a JSON example in a prompt must not crash the imagen adapter. Tests live in `tests/test_brace_policy.py`.

## Why this exists

`gemini-imagen` treats `{name}` as a template variable and runs `str.format`.
A single brace in a prompt is a merge bug. grok-img and Codex agent prompts do
not need the rewrite. Copying the wrong escape is the first production failure.

## Invocations

imagen (gemini-imagen, no `--prompt-file` yet):

```text
imagen generate PROMPT -o OUT --aspect-ratio 16:9 -m gemini-3.1-flash-image
```

imagen (if `--prompt-file` is in `--help`):

```text
imagen generate --prompt-file FILE --aspect-ratio 16:9 -o OUT -m MODEL
```

grok:

```text
grok-img generate PROMPT --aspect-ratio 16:9 --count 1 --output STAGING_DIR
```

The plugin stages grok-img output in an isolated directory, then copies the
single generated image to `OUT`. `grok-img auth login` or `XAI_API_KEY` is
required. The official Grok Build TUI `/imagine` command is interactive and is
not the script adapter.

codex:

```text
codex exec --skip-git-repo-check --ephemeral --add-dir OUT_PARENT -
```

The prompt is passed on stdin and tells the Codex host to use `image_gen` and
save exactly `OUT`. The adapter checks that the file exists after Codex exits.
