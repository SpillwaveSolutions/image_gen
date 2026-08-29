# Backends and brace policy

## Auto order

1. `imagen` if on PATH. Policy `imagen-cli-vars`.
2. Else `grok` if on PATH. Policy `grok-imagine`.
3. Else `codex` if on PATH. Policy `grok-imagine`.
4. Else fail closed. Write `<stem>_imagen.prompt.txt` and exit 2.

Pin with `--backend imagen|grok|codex|imagen-scan|auto`.

`imagen-scan` rewrites `{token}` to `(token)` for binaries that still scan the inner token.

## Policies

```text
imagen-cli-vars     -> double every { and }
imagen-cli-scan     -> rewrite {token} to (token)
grok-imagine        -> no brace rewrite
```

A `{Decision?}` node or a JSON example in a prompt must not crash the imagen adapter. Tests live in `tests/test_brace_policy.py`.

## Why this exists

`gemini-imagen` treats `{name}` as a template variable and runs `str.format`. A single brace in a prompt is a merge bug. Grok Imagine and Codex image generate do not. Copying the wrong escape is the first production failure.

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
grok imagine generate --prompt-file FILE --aspect 16:9 --output OUT
```

codex:

```text
codex image generate --prompt-file FILE --aspect 16:9 --output OUT
```
