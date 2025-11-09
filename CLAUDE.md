# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Claude Code skill for generating high-quality images for technical articles using the `imagen` CLI tool (powered by `gemini-2.5-flash-image`). The skill provides systematic workflows for creating both cover images and in-article illustrations with comprehensive prompt engineering guidance.

## Core Commands

### Image Generation

```bash
# Basic image generation
imagen generate "DETAILED PROMPT" --output FILENAME.png

# Example: Cover image
imagen generate "A stunning digital art cover image showing three glowing pathways converging into a central AI cloud platform. Dramatic cinematic lighting, futuristic tech aesthetic. Style: conceptual, 3D render, high-detail, professional." --output work/images/article_cover.png

# Example: Technical diagram
imagen generate "Technical diagram showing three color-coded client libraries connecting to central platform. Clear labels and arrows. Style: blueprint, technical diagram, clean." --output work/images/diagram.png
```

### Directory Setup

```bash
# Create image output directory
mkdir -p work/images
```

## Architecture and Workflow

### Two-Phase Image Strategy

1. **Cover Images**: High-impact, conceptual images for grabbing attention on social platforms (LinkedIn/Medium)
   - Style: `digital art`, `3D render`, `conceptual art`, `abstract`
   - Approach: Metaphorical and dramatic
   - Keywords: `cinematic lighting`, `futuristic`, `professional`

2. **In-Article Images**: Technical diagrams and illustrations for explaining concepts
   - Style: `technical diagram`, `blueprint`, `minimalist illustration`
   - Approach: Direct and educational
   - Keywords: `clear labels`, `organized`, `clean`

### Standard Workflow Execution

1. **Analyze Article**: Identify key themes and concepts needing visualization
2. **Generate Cover**: Create one high-impact conceptual image
3. **Generate In-Article Images**: Create 1-3 technical diagrams/illustrations
4. **Integrate with ALT Text**: Add SEO-friendly descriptive ALT text (50-125 chars)
5. **Save Updated Article**: Version with integrated images

### Prompt Engineering Principles

Core principles from `references/prompting_guide.md`:

1. **Be Specific**: Detailed descriptions (100+ words acceptable)
2. **Define Style**: Always specify artistic style explicitly
3. **Set Atmosphere**: Use lighting and mood keywords
4. **Use Photography Terms**: `wide-angle`, `close-up`, `depth of field`

**Prompt Structure for Covers**:
```
[Style] cover image of [Metaphor/Concept] representing [Article Topic], [Atmosphere/Lighting], [Composition]
```

**Prompt Structure for Diagrams**:
```
[Style] showing [Specific Concept], [Visual Elements], [Labels/Clarity]
```

### SEO-Friendly ALT Text

**Good Examples**:
- "Architecture diagram showing Cloud Run connecting through VPC Connector to AlloyDB in private subnet"
- "Comparison showing manual infrastructure with tangled wires versus automated infrastructure-as-code"

**Bad Examples** (avoid):
- "diagram" or "image"
- "architecture" (too vague)
- "image1.png"

## File Structure

```
image-gen/
├── SKILL.md                    # Skill definition and comprehensive documentation
├── CLAUDE.md                   # This file
├── README.md                   # User-facing documentation
├── references/
│   └── prompting_guide.md     # Detailed prompt engineering guide
└── scripts/                    # (Empty - placeholder for future automation)
```

## Integration with Articles

Images should be integrated into markdown with this pattern:

```markdown
# Article Title

![Conceptual cover image showing three glowing AI model pathways converging into Google Cloud platform](images/vertex_ai_cover.png)

## Introduction

Text introducing the problem...

![Technical diagram illustrating three-client pattern with color-coded SDK connections to Vertex AI](images/vertex_ai_three_patterns.png)
```

## Common Patterns

**Pattern 1: Simple Article**
- Cover image only

**Pattern 2: Standard Article**
- Cover image (conceptual)
- 1-2 in-article images (technical diagrams)

**Pattern 3: Complex Tutorial**
- Cover image (conceptual)
- Workflow/architecture diagram
- Comparison illustration
- Example/output visualization

## Important Notes

- The `imagen` CLI requires Python 3.12.9+ (managed via pyenv)
- All prompts should include explicit style keywords
- Cover images use metaphorical/conceptual approaches
- In-article images use direct/educational approaches
- Always provide descriptive ALT text for accessibility and SEO
- Save articles with version numbers when adding images (e.g., `v8_with_images.md`)

## Reference Documentation

- **SKILL.md**: Complete skill documentation with workflow details
- **references/prompting_guide.md**: Comprehensive prompt engineering guide with examples and best practices
