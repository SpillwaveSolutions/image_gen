# Prompting guide for article images

Use `generate.py` so backend detection, brace policy, and fail-closed behavior stay intact. Direct `imagen generate` still works when `imagen` is on PATH.

```bash
python3 skills/image-gen/scripts/generate.py \
  --kind cover \
  --output work/images/article_cover.png \
  --prompt "YOUR PROMPT HERE"
```

Default model is Nano Banana 2 (`gemini-3.1-flash-image`). Covers use Nano Banana Pro (`gemini-3-pro-image`) because in-image text and dense composition hold up better.

If the prompt contains `{` or `}`, do not hand-escape it. `generate.py` applies `imagen-cli-vars` or `grok-imagine` from the detected backend.

## Core principles

### 1. Be specific

- Simple: `A server.`
- Compelling: `A single sleek modern server rack with glowing blue LED lights, standing in a clean dark futuristic data center.`

### 2. Name the style

Keywords: `photorealistic`, `digital art`, `technical diagram`, `blueprint style`, `watercolor illustration`, `3D render`, `minimalist line art`, `abstract`, `conceptual art`.

### 3. Set lighting and atmosphere

Keywords: `cinematic lighting`, `dramatic lighting`, `soft natural light`, `backlit`, `glowing`, `neon glow`, `dark and moody`, `bright and optimistic`.

### 4. Direct the camera

Keywords: `wide-angle shot`, `close-up macro shot`, `from a low angle`, `top-down view`, `portrait`, `landscape`, `depth of field`, `motion blur`.

## Cover images

Goal: grab attention. Metaphorical, not literal.

Structure: `[Style] cover image of [Metaphor] representing [Topic], [Atmosphere], [Composition].`

Example (AI ethics):

```
A stunning digital art cover image of a classic Greek statue holding a glowing intricate neural network in its hands. The statue is cracked, showing circuits underneath. Dramatic spotlight in a dark room. Style: conceptual, cinematic, high-detail.
```

Use `--kind cover` (Nano Banana Pro). 16:9.

## In-article images

Goal: explain one concept. Direct, labeled, clean.

Example (architecture):

```
A detailed system architecture diagram for a URL shortening service. Show a load balancer, web servers, a hash generation service, a distributed NoSQL store, and a Redis cache. Clear labels and connecting arrows. Style: clean blueprint, technical diagram.
```

Example (abstract point):

```
A minimalist illustration showing a small sapling growing out of a discarded computer keyboard, symbolizing new ideas from old technology. Style: clean, simple color palette, symbolic.
```

Ask for "clear labels" on Pro. On Flash, keep labels short or skip small text.

## Cover vs in-article

| Aspect | Cover | In-article |
| --- | --- | --- |
| Goal | Attention | Explanation |
| Style | digital art, 3D render, conceptual | technical diagram, blueprint, minimalist |
| Approach | Metaphor | One concept, labeled |
| Model | nano-banana-pro | nano-banana-2 |
