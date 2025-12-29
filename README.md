# Image Gen - AI-Powered Article Image Generation

Generate high-quality cover images and technical diagrams for your articles using the `imagen` CLI tool powered by `gemini-2.5-flash-image`.

[![Skilz Marketplace](https://img.shields.io/badge/Skilz-Marketplace-blue)](https://skillzwave.ai/skill/SpillwaveSolutions__image_gen__image-gen__SKILL/)
[![GitHub](https://img.shields.io/badge/GitHub-SpillwaveSolutions%2Fimage__gen-black)](https://github.com/SpillwaveSolutions/image_gen)

## Overview

This Claude Code skill provides a systematic workflow for creating two types of images for technical articles:

1. **Cover Images**: High-impact, conceptual images that grab attention on LinkedIn/Medium
2. **In-Article Images**: Technical diagrams and illustrations that explain specific concepts

The skill includes comprehensive prompt engineering guidance and best practices for integrating images with SEO-friendly ALT text.

## Installation

### Universal Installer (Recommended)

The easiest way to install this skill is using the [skilz universal installer](https://github.com/AgenDev-Inc/skilz):

```bash
skilz install SpillwaveSolutions_image_gen/image-gen
```

This will automatically download and configure the skill for use with Claude Code.

### Manual Installation

Alternatively, you can manually clone the repository to your Claude Code skills directory:

```bash
git clone https://github.com/SpillwaveSolutions/image_gen.git ~/.claude/skills/image-gen
```

## Prerequisites

- Python 3.12.9+ (managed via pyenv)
- `imagen` CLI tool installed
- Claude Code environment

## Quick Start

```bash
# Generate a cover image
imagen generate "A stunning digital art cover image of [your concept]..." --output work/images/cover.png

# Generate a technical diagram
imagen generate "Technical diagram showing [your concept]..." --output work/images/diagram.png
```

## Workflow

### 1. Analyze Your Article

Identify:
- Main topic and key themes
- Complex concepts needing visualization
- Optimal section breaks for images
- Target audience level

### 2. Generate Cover Image

Cover images should be **conceptual and visually striking**:

```bash
imagen generate "A stunning digital art cover image showing three glowing pathways (green, blue, gold) converging into a central AI cloud platform. Dramatic cinematic lighting, futuristic tech aesthetic. Style: conceptual, 3D render, high-detail, professional." --output work/images/article_cover.png
```

**Style keywords**: `digital art`, `3D render`, `conceptual art`, `cinematic lighting`

### 3. Generate In-Article Images

In-article images should be **clear and educational**:

```bash
imagen generate "Technical diagram showing three color-coded client libraries connecting to central platform with clear labels and arrows. Style: blueprint, technical diagram, clean." --output work/images/diagram.png
```

**Style keywords**: `technical diagram`, `blueprint`, `minimalist`, `clear labels`

### 4. Integrate with ALT Text

Add images to your markdown with descriptive ALT text:

```markdown
# Article Title

![Conceptual image showing three glowing pathways converging into cloud platform](images/cover.png)

## Section

Text content...

![Technical diagram illustrating three-client pattern with color-coded connections](images/diagram.png)
```

**Good ALT Text** (50-125 characters):
- "Architecture diagram showing Cloud Run connecting to AlloyDB via VPC Connector"
- "Comparison of manual infrastructure versus infrastructure-as-code automation"

**Bad ALT Text**:
- "diagram" or "image"
- "screenshot" or "image1.png"

## Prompt Engineering Tips

### For Cover Images

**Goal**: Grab attention with metaphorical, dramatic visuals

**Structure**:
```
[Style] cover image of [Metaphor/Concept] representing [Topic], [Atmosphere/Lighting], [Composition]
```

**Example**:
```
A dramatic 3D render showing a database schema transforming like evolving architecture, with migration files as glowing blueprints guiding the transformation. Dark background with cinematic lighting. Style: conceptual art, digital art, high-detail, professional.
```

### For In-Article Images

**Goal**: Explain concepts clearly and directly

**Structure**:
```
[Style] showing [Specific Concept], [Visual Elements], [Labels/Clarity]
```

**Example**:
```
A clean technical diagram showing three distinct client libraries connecting to a central platform. Use color-coded arrows and clear labels for each connection path. Style: blueprint, technical diagram, professional.
```

### Key Principles

1. **Be Specific**: Detailed descriptions produce better results (100+ words is fine)
2. **Define Style**: Always specify artistic style explicitly
3. **Set Atmosphere**: Use lighting and mood keywords
4. **Use Visual Language**: `wide-angle`, `close-up`, `depth of field`, `connecting arrows`

## Common Image Patterns

### Pattern 1: Simple Article (1-2 images)
- Cover image only
- OR Cover + 1 key diagram

### Pattern 2: Standard Article (2-3 images)
- Cover image (conceptual)
- 1-2 in-article images (technical diagrams)

### Pattern 3: Complex Tutorial (3-4 images)
- Cover image (conceptual)
- Workflow/architecture diagram
- Comparison illustration
- Example/output visualization

## Complete Example

For an article on "Mastering Vertex AI":

```bash
# Step 1: Create output directory
mkdir -p work/images

# Step 2: Generate cover
imagen generate "A stunning digital art cover image showing three glowing pathways (green, blue, gold) converging into a central AI cloud platform representing Google Vertex AI. Dramatic cinematic lighting, futuristic tech aesthetic. Style: conceptual, 3D render, high-detail, professional." --output work/images/vertex_ai_cover.png

# Step 3: Generate technical diagram
imagen generate "Technical diagram showing three color-coded client libraries (green: Google SDK, blue: Anthropic SDK, gold: OpenAI SDK) connecting to central Vertex AI platform. Clear labels and arrows. Style: blueprint, technical diagram, clean." --output work/images/vertex_ai_diagram.png

# Step 4: Generate comparison
imagen generate "Side-by-side comparison: left shows traditional API integration with multiple adapters, right shows unified Vertex AI approach. Clean, minimalist. Style: minimalist illustration, professional." --output work/images/vertex_ai_comparison.png
```

Then integrate into markdown:

```markdown
# Mastering Google Vertex AI: Three Client Patterns

![Conceptual image showing three glowing pathways converging into central AI cloud platform](images/vertex_ai_cover.png)

## Introduction

Problem statement...

![Technical diagram illustrating three client libraries with color-coded connections to Vertex AI](images/vertex_ai_diagram.png)

## Traditional vs Unified Approach

Comparison content...

![Comparison showing traditional multi-adapter API integration versus unified Vertex AI approach](images/vertex_ai_comparison.png)
```

## Style Comparison

| Aspect | Cover Images | In-Article Images |
|--------|-------------|-------------------|
| **Goal** | Grab attention | Explain concepts |
| **Style** | `digital art`, `3D render`, `conceptual art` | `technical diagram`, `blueprint`, `minimalist` |
| **Approach** | Metaphorical, abstract | Direct, educational |
| **Keywords** | `cinematic`, `dramatic`, `futuristic` | `clean`, `clear labels`, `organized` |

## Additional Resources

- **SKILL.md**: Complete skill documentation with detailed workflow
- **references/prompting_guide.md**: Comprehensive prompt engineering guide with examples

## Tips for Best Results

1. **Be detailed in prompts** - More description = better results
2. **Specify style explicitly** - Never assume a default style
3. **Use color-coding** - Helps distinguish elements in diagrams
4. **Request clear labels** - Essential for technical diagrams
5. **Think metaphorically** - For cover images, find visual metaphors
6. **Keep it simple** - One concept per image for in-article illustrations
7. **Test and iterate** - Generate multiple versions if needed

## Links

- **Skilz Marketplace**: [https://skillzwave.ai/skill/SpillwaveSolutions__image_gen__image-gen__SKILL/](https://skillzwave.ai/skill/SpillwaveSolutions__image_gen__image-gen__SKILL/)
- **GitHub Repository**: [https://github.com/SpillwaveSolutions/image_gen](https://github.com/SpillwaveSolutions/image_gen)

## License

This skill is part of the Claude Code ecosystem.
