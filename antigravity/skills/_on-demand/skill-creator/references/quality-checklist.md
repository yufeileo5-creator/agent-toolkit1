# Skill Quality Checklist

When reviewing a generated Agent Skill, evaluate it against the following criteria:

## 1. Metadata Quality (YAML Frontmatter)
- [ ] **Completeness**: Does it contain `name` and `description`?
- [ ] **Precision**: Is the `description` highly specific? Does it clearly specify the trigger condition to prevent false positives during auto-matching?

## 2. Inversion Pattern (反转保护)
- [ ] **Guards**: If the skill is complex, does it have explicit directives like `DO NOT proceed until user confirms`?

## 3. Abstraction & Decoupling (Tool Wrapper)
- [ ] **File Size**: Is `SKILL.md` kept concise?
- [ ] **Separation of Concerns**: Are large lists of rules moved to `references/*.md`? Are output templates moved to `assets/*.md`?

## 4. Pipeline Strictness (流水线)
- [ ] **Sequential Steps**: If the skill involves a multi-step workflow, are the steps strictly numbered (Step 1, Step 2)?
- [ ] **Skip Prevention**: Does it explicitly state `Execute each step in order. Do NOT skip steps.`?

## 5. Review Criteria (审查机制)
- [ ] **Self-Reflection**: Does the skill mandate the Agent to evaluate its own final output against the specific criteria before handoff?

## 6. Advanced Quality Controls (高阶心法)
- [ ] **Single Responsibility (单一职责)**: Is the skill highly cohesive? (If it mixes generation, architecture planning, and reviewing all in one, it MUST be split into multiple smaller skills).
- [ ] **Gotchas Section (避坑清单)**: Does the generated `SKILL.md` explicitly contain a `## Gotchas / Common Pitfalls` section to suppress specific known LLM hallucinations?
- [ ] **Statefulness & Hooks (状态与防呆)**: If it's a long pipeline, does it enforce State Logging (e.g., Micro-Commits / disk logs) or explicit user confirmation Hooks before moving to the next risk node?
