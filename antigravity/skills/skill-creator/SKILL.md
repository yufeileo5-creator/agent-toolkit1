---
name: skill-creator
description: 创建或优化 Agent Skill 时触发。遵循标准 SKILL.md 格式，包含 description 优化、目录结构和质量验证最佳实践。
---

# Skill Creator Guide

Create effective, well-structured skills that extend agent capabilities with
specialized knowledge, workflows, or tool integrations.

## When to Use

- Creating a new skill from scratch
- Editing or improving an existing skill
- Optimizing a skill's description for better auto-matching

## Skill Structure

A skill is a directory containing at minimum a `SKILL.md` file:

```
skills/
└── my-skill/
    ├── SKILL.md          # Required: Instructions + metadata
    ├── scripts/          # Optional: Helper scripts
    ├── examples/         # Optional: Reference implementations
    ├── reference/        # Optional: Documentation resources
    └── resources/        # Optional: Templates, assets, etc.
```

## SKILL.md Format

The `SKILL.md` file has two parts:

### 1. YAML Frontmatter (Metadata)

```yaml
---
name: my-skill-name
description: >-
  A clear, concise description of what this skill does and when it
  should be activated. This is used for auto-matching user requests
  to skills. Be specific about trigger conditions.
---
```

**Description best practices:**
- Start with an action verb ("Guide for...", "Use when...", "Create...")
- Include trigger keywords that users would naturally say
- Be specific about when the skill activates
- Keep it under 200 characters for optimal matching

### 2. Markdown Body (Instructions)

The body contains the actual instructions the agent follows. Structure it as:

```markdown
# Skill Title

Brief overview of the skill's purpose and approach.

## Prerequisites
What needs to be in place before using this skill.

## Workflow / Process
Step-by-step instructions organized into phases.

## Best Practices
Guidelines, patterns, and anti-patterns.

## Reference Files
Links to supporting documentation.
```

## Creating a High-Quality Skill

### Phase 1: Define Purpose
1. **Identify the gap**: What capability is missing?
2. **Define the trigger**: When should this skill activate?
3. **Scope the skill**: What are the boundaries? What is NOT included?

### Phase 2: Write Instructions
1. **Be imperative**: Write clear, actionable instructions
2. **Use decision trees**: Help the agent choose the right path
3. **Include examples**: Show expected inputs and outputs
4. **Add guardrails**: Specify what NOT to do
5. **Reference external docs**: Link to resources instead of embedding them

### Phase 3: Optimize Description
1. **Test matching**: Try various user prompts to see if the skill activates
2. **Add trigger words**: Include keywords users would naturally use
3. **Differentiate**: Make the description distinct from other skills

### Phase 4: Validate
1. **Dry run**: Test the skill end-to-end with a real scenario
2. **Edge cases**: Test with unusual inputs
3. **Review output quality**: Ensure consistent, high-quality results

## Anti-Patterns to Avoid

- ❌ **Overly broad descriptions** that match too many unrelated requests
- ❌ **Embedding large reference docs** directly in SKILL.md (link instead)
- ❌ **Vague instructions** like "do the right thing"
- ❌ **Missing guardrails** that let the agent go off-track
- ❌ **Monolithic skills** that try to do too much (split into focused skills)

## Skill Description Optimization

The `description` field is the single most important factor for skill
auto-matching. Optimize it by:

1. **Including action verbs**: "Use when building...", "Activate when..."
2. **Listing trigger scenarios**: "...when user mentions X, Y, or Z"
3. **Being specific**: "PDF files" not "documents"
4. **Testing recall**: Verify the skill activates for intended queries
5. **Testing precision**: Verify it does NOT activate for unintended queries

## Template

Use this template as a starting point:

```markdown
---
name: my-skill
description: >-
  [Action verb] [what it does]. Use when [trigger conditions].
  [Additional context about when to activate].
---

# [Skill Title]

[1-2 sentence overview of purpose and approach]

## Prerequisites
- [Required tools, dependencies, or conditions]

## Workflow

### Step 1: [Phase Name]
[Clear, imperative instructions]

### Step 2: [Phase Name]
[Clear, imperative instructions]

## Best Practices
- [Guideline 1]
- [Guideline 2]

## Common Pitfalls
- ❌ [Anti-pattern to avoid]
- ✅ [Correct approach instead]
```
