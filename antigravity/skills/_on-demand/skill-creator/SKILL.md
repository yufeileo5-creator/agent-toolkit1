---
name: skill-creator
description: 专门用于创建或重构 Agent Skill 的超级流水线（Tier 2 按需加载）。采用 5 种高阶设计模式进行严格的质量控制。当需要编写新技能或修改原有技能时触发。
---

# Skill Creator Pipeline

You are executing a rigorous pipeline to create or refactor an Agent Skill. 
DO NOT skip any steps. You MUST strictly follow the Inversion, Generator, and Reviewer patterns.

## Step 1: Requirements Inversion (先问再做)
**DO NOT generate any code or documentation until Step 1 is thoroughly completed.**
Ask the user the following questions sequentially (you can combine them in one message, but wait for the answer):
1. **Scope & Location**: Is this a Global Agent Skill (stored in `~/.gemini/antigravity/skills/`) or a **Project-Local Built-in Skill** (stored inside the current project's repository, e.g., `./.agents/skills/` or `./.golden-rules/`)?
2. **Trigger Condition**: What exactly should trigger this skill? (If global, is it Tier 1/2/3? If local, does it trigger on specific file modifications?)
3. **Design Pattern**: Which of the 5 design patterns suit this skill best? (Tool Wrapper, Generator, Reviewer, Inversion, Pipeline, or a combination?)
4. **Complexity & Dependencies**: Does it need external reference files (`references/*.md`) or templates (`assets/*.md`)?

*Wait for the user's response before proceeding to Step 2.*

## Step 2: Generator (模板生成)
Once requirements are gathered:
1. Create the `SKILL.md` with the standard YAML frontmatter:
   - `name`: string
   - `description`: A highly precise description stating exactly when to drop into this skill. This must be under 200 characters and contain trigger keywords.
2. If the user requires specific instructions, place them clearly under standard markdown headings.
   - **MUST INCLUDE**: A `## Gotchas / Common Pitfalls` (避坑指南) section to explicitly document known AI hallucinations or common mistakes to avoid.
   - **For Pipelines**: Include instructions for "Statefulness" (e.g., mandate writing step conclusions to a local `.log` file or triggering `Micro-Commits` between phases).
   - **For Destructive Actions**: Define clear Security Guardrails/Hooks (e.g., "Wait for user confirmation before running `rm` or pushing code").
3. For heavy checklists or templates, DO NOT hardcode them inside `SKILL.md`. Instead, generate:
   - `references/[name].md` for rules and criteria.
   - `assets/[name].md` for format templates.
   and use phrases like "Load 'references/xxx.md'" in the `SKILL.md`.

## Step 3: Reviewer (质检自审)
Before presenting the final output to the user, load your generated output and evaluate it against our internal Skill Quality Checklist. 
Execute exactly as follows:
1. Load `references/quality-checklist.md` relative to this skill's directory (`skills/_on-demand/skill-creator/references/quality-checklist.md`).
2. Review your generated `SKILL.md` against every point.
3. Fix any violations automatically.
4. Output the final summary of what was generated, including the files created and the validation score.
