# Prompt Optimizer Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a shareable Claude Code plugin, `prompt-optimizer`, that optimizes/standardizes prompts against Claude's documented best practices plus a project house style, via an interactive optimizer and a project scanner.

**Architecture:** One bundled ruleset (`reference/best-practices.md`) is the single source of truth. Two thin front-ends read it: an `optimize-prompt` skill (interactive, modes A+C) and a `scan-prompts` skill that dispatches a `prompt-scanner` subagent (mode B). A house-style config in the user's project layers on top.

**Tech Stack:** Claude Code plugin format (markdown skills/agents + JSON manifest). No runtime/build step. "Tests" are structural validation (`claude plugin validate`, JSON/frontmatter parsing) plus manual fixture review, since outputs are non-deterministic.

## Global Constraints

- Plugin manifest lives ONLY at `.claude-plugin/plugin.json`; all other dirs at plugin root.
- Plugin name: `prompt-optimizer`. Skills invoked as `/prompt-optimizer:<skill>`.
- Bundled files referenced via `${CLAUDE_PLUGIN_ROOT}`; project root via `${CLAUDE_PROJECT_DIR}`.
- House-style config path in a user project: `.prompt-optimizer/house-style.md`.
- Best practices are BUNDLED (offline, version-pinned), citing source URL: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Scanner is suggest-and-apply-on-approval: never edits a file without explicit user confirmation.
- Commit after each task.

---

## File Structure

| File | Responsibility |
|------|----------------|
| `.claude-plugin/plugin.json` | Plugin manifest |
| `.gitignore` | Ignore OS/editor cruft |
| `reference/best-practices.md` | The distilled ruleset (single source of truth) |
| `reference/house-style-template.md` | Default/example house style |
| `skills/optimize-prompt/SKILL.md` | Interactive optimizer (modes A + C) |
| `skills/init-house-style/SKILL.md` | Scaffolds house-style config into a project |
| `skills/scan-prompts/SKILL.md` | Entry point for mode B; dispatches subagent |
| `agents/prompt-scanner.md` | Subagent: discover prompts → evaluate → propose diffs |
| `tests/fixtures/optimize/` | Before/after fixture prompts for manual review |
| `tests/sample-project/` | Tiny project with embedded prompts for scanner check |
| `README.md` | Usage + install docs |

---

## Task 1: Manifest + repo scaffolding

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `.gitignore`

**Interfaces:**
- Produces: a valid plugin root discoverable by `claude --plugin-dir .`

- [ ] **Step 1: Create `.claude-plugin/plugin.json`**

```json
{
  "name": "prompt-optimizer",
  "displayName": "Prompt Optimizer",
  "description": "Optimize and standardize prompts against Claude's prompt-engineering best practices plus your project's house style.",
  "version": "0.1.0",
  "author": { "name": "Nirav Sangani" },
  "keywords": ["prompt-engineering", "optimization", "standardization", "best-practices", "claude"],
  "license": "MIT"
}
```

- [ ] **Step 2: Create `.gitignore`**

```gitignore
# OS / editor
.DS_Store
Thumbs.db
*.swp
.idea/
.vscode/

# Logs / temp
*.log
.tmp/
```

- [ ] **Step 3: Validate JSON**

Run: `node -e "JSON.parse(require('fs').readFileSync('.claude-plugin/plugin.json','utf8')); console.log('ok')"`
Expected: `ok`

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/plugin.json .gitignore
git commit -m "feat: add plugin manifest and gitignore"
```

---

## Task 2: Best-practices ruleset (single source of truth)

**Files:**
- Create: `reference/best-practices.md`

**Interfaces:**
- Produces: a named ruleset consumed by `optimize-prompt` and `prompt-scanner`. Stable group headings (10) used by verification.

- [ ] **Step 1: Create `reference/best-practices.md`** with exactly these sections and content (each rule named; faithful to the source doc):

```markdown
# Claude Prompt-Engineering Best Practices (distilled)

Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
Distilled: 2026-06-28. Applies to current Claude models (Fable 5, Opus 4.8, Sonnet 4.6, Haiku 4.5). Model-specific notes are labelled.

When optimizing a prompt, evaluate it against every rule below. For each change, cite the rule name in the rationale.

## 1. Clarity & directness
- **be-explicit**: Give clear, specific instructions; treat Claude as a capable new hire lacking your context. State desired output and constraints exactly.
- **request-above-and-beyond**: If you want fully-featured output, ask for it explicitly (e.g. "Include as many relevant features as possible") rather than relying on inference.
- **sequential-steps**: When order/completeness matters, give steps as a numbered or bulleted list.
- **colleague-test**: A prompt a low-context colleague would find confusing will confuse Claude too.

## 2. Context & motivation
- **explain-why**: State the motivation behind an instruction; Claude generalizes from the explanation (e.g. "...read aloud by TTS, so never use ellipses").

## 3. Examples (few-shot / multishot)
- **use-examples**: Add 3–5 examples to steer format, tone, structure.
- **examples-relevant-diverse**: Make examples mirror the real use case and cover edge cases without leaking unintended patterns.
- **examples-tagged**: Wrap each example in `<example>` tags (`<examples>` around the set).

## 4. XML structure
- **xml-tags**: Wrap distinct content types in their own descriptive tags (`<instructions>`, `<context>`, `<input>`).
- **xml-consistent-nested**: Use consistent tag names; nest tags for natural hierarchy.

## 5. Role / system prompt
- **set-role**: Set a role in the system prompt to focus tone and behavior; even one sentence helps.

## 6. Long-context handling (20k+ tokens)
- **data-on-top**: Put long documents/inputs near the top, above the query and instructions.
- **query-at-bottom**: Place the actual question/instructions after the data (can improve quality up to ~30%).
- **document-metadata-tags**: Wrap each document in `<document>` with `<source>` and `<document_content>` subtags.
- **ground-in-quotes**: For long-document tasks, ask Claude to extract relevant quotes first (in `<quotes>` tags) before answering.

## 7. Output & formatting
- **say-what-to-do**: Tell Claude what to do, not what to avoid ("write flowing prose" beats "don't use markdown").
- **xml-format-indicators**: Use tags like `<smoothly_flowing_prose_paragraphs>` to mark desired output shape.
- **match-prompt-style**: Match the prompt's own formatting to the desired output style.
- **explicit-format-guidance**: For strict formatting, give detailed explicit guidance.
- **prefer-structured-outputs**: Don't rely on prefill (deprecated on 4.6+); use Structured Outputs / tool enums for schemas and "respond without preamble" to drop preambles.

## 8. Tool use
- **explicit-action**: To make Claude act (not just suggest), use imperative phrasing ("Change this function", not "Can you suggest changes").
- **avoid-over-prompting**: Don't use "CRITICAL/MUST" pressure; modern models overtrigger. Use normal phrasing ("Use this tool when...").
- **parallel-tool-calls**: Encourage parallel independent tool calls; require sequential only for dependent calls.

## 9. Thinking & reasoning
- **calibrate-thoroughness**: Replace blanket "always use X" with targeted "use X when it helps"; remove anti-laziness over-prompting.
- **adaptive-thinking**: Prefer adaptive thinking; control depth via `effort`, not `budget_tokens` (deprecated/400 on newer models).
- **self-check**: Ask Claude to verify its answer against criteria before finishing.
- **cot-fallback-tags**: When thinking is off, request step-by-step reasoning using `<thinking>` and `<answer>` tags. Note: on Opus 4.5 with thinking off, prefer "consider/evaluate/reason through" over "think".

## 10. Agentic safety & quality
- **confirm-destructive**: Instruct confirmation before destructive/irreversible/shared-system actions; never bypass safety checks as a shortcut.
- **avoid-overengineering**: Keep solutions minimal; no unrequested features, abstractions, defensive code, or docs.
- **no-test-hardcoding**: Solve the general problem, not just the test cases; report bad/infeasible tests instead of working around them.
- **investigate-before-answering**: Never speculate about unopened code; read referenced files before answering.
- **state-tracking** (long-horizon): Use structured files (e.g. `tests.json`) for state, freeform notes for progress, git for checkpoints; emphasize incremental progress.
```

- [ ] **Step 2: Verify all 10 group headings present**

Run: `grep -cE "^## [0-9]+\. " reference/best-practices.md`
Expected: `10`

- [ ] **Step 3: Commit**

```bash
git add reference/best-practices.md
git commit -m "feat: add distilled best-practices ruleset"
```

---

## Task 3: House-style template

**Files:**
- Create: `reference/house-style-template.md`

**Interfaces:**
- Produces: the template copied by `init-house-style` to `.prompt-optimizer/house-style.md`; consumed by both front-ends as the house-style layer.

- [ ] **Step 1: Create `reference/house-style-template.md`**

```markdown
# Prompt house style

This file defines project-specific prompt conventions layered ON TOP of Claude's
best practices. The optimizer applies best practices first, then enforces these.
House style may tighten or specialize defaults but must not override safety guidance.

Edit the sections below to match your project. Delete any you don't need.

## Tone & voice
- (e.g.) Direct, concise, no marketing language.

## Required prompt sections
List the sections every standardized prompt in this project should contain, in order.
- (e.g.) `<role>`, `<context>`, `<instructions>`, `<constraints>`, `<output_format>`

## Default output format
- (e.g.) Return JSON matching the documented schema; no prose preamble.

## Tag & naming conventions
- (e.g.) Use snake_case XML tag names; use `<example>` for samples.

## Forbidden patterns
- (e.g.) No "CRITICAL/MUST" pressure language; no prefilled assistant turns; no ellipses.

## Project glossary / domain notes
- (e.g.) Terms the model should use consistently.
```

- [ ] **Step 2: Verify required headings present**

Run: `grep -cE "^## " reference/house-style-template.md`
Expected: `6`

- [ ] **Step 3: Commit**

```bash
git add reference/house-style-template.md
git commit -m "feat: add house-style template"
```

---

## Task 4: `optimize-prompt` skill (modes A + C)

**Files:**
- Create: `skills/optimize-prompt/SKILL.md`

**Interfaces:**
- Consumes: `reference/best-practices.md`, `${CLAUDE_PROJECT_DIR}/.prompt-optimizer/house-style.md` (optional), `reference/house-style-template.md` (fallback).
- Produces: a 3-part response (rewritten prompt, rationale citing rules, issues checklist).

- [ ] **Step 1: Create `skills/optimize-prompt/SKILL.md`**

```markdown
---
description: Optimize and standardize a prompt against Claude's prompt-engineering best practices and the project house style. Use when the user wants to improve, rewrite, audit, or standardize a single prompt.
argument-hint: "the prompt text to optimize (or omit to be asked for it)"
allowed-tools: Read, Glob, Grep
---

# Optimize prompt

You optimize/standardize a prompt against Claude's best practices plus the project house style.

## Inputs
- The prompt to optimize is in `$ARGUMENTS`. If `$ARGUMENTS` is empty, ask the user to paste the prompt and stop until they do.

## Procedure
1. Read the ruleset: `${CLAUDE_PLUGIN_ROOT}/reference/best-practices.md`.
2. Load house style: read `${CLAUDE_PROJECT_DIR}/.prompt-optimizer/house-style.md`. If it does not exist, read `${CLAUDE_PLUGIN_ROOT}/reference/house-style-template.md` as a fallback and tell the user they can run `/prompt-optimizer:init-house-style` to create a project-specific one.
3. If you are inside a project (a `${CLAUDE_PROJECT_DIR}` with source files), gather LIGHT context only when it helps tailor the prompt: detect the stack/conventions and, if the prompt references project concepts, skim the most relevant file(s). Do not do a full scan. Skip this entirely for a generic pasted prompt.
4. Evaluate the prompt against EVERY rule group in the ruleset. Note which rules it already follows and which it violates.
5. Produce the output in exactly three parts:

### Optimized prompt
Output the rewritten prompt in a single fenced code block, copy-ready. Apply the violated rules and the house style. Do not invent requirements the user did not state; if information is genuinely missing, add a clearly marked `{{PLACEHOLDER}}` rather than guessing.

### What changed and why
A short bulleted list. Each bullet names the rule applied (e.g. `set-role`, `xml-tags`) and what you changed.

### Checklist
A compact checklist of the rule groups, marking which were already satisfied vs improved.

## Rules of engagement
- This skill is non-destructive: never edit files. You only return text.
- Preserve the user's intent and constraints; standardize form, do not change meaning.
- Keep house style subordinate to safety guidance in the ruleset.
```

- [ ] **Step 2: Verify frontmatter parses and references the ruleset**

Run: `grep -q "CLAUDE_PLUGIN_ROOT}/reference/best-practices.md" skills/optimize-prompt/SKILL.md && head -1 skills/optimize-prompt/SKILL.md`
Expected: first line is `---` and command exits 0.

- [ ] **Step 3: Commit**

```bash
git add skills/optimize-prompt/SKILL.md
git commit -m "feat: add optimize-prompt skill"
```

---

## Task 5: `init-house-style` skill

**Files:**
- Create: `skills/init-house-style/SKILL.md`

**Interfaces:**
- Consumes: `reference/house-style-template.md`.
- Produces: `${CLAUDE_PROJECT_DIR}/.prompt-optimizer/house-style.md`.

- [ ] **Step 1: Create `skills/init-house-style/SKILL.md`**

```markdown
---
description: Scaffold a prompt-optimizer house-style config into the current project so prompts can be standardized to project conventions.
allowed-tools: Read, Write, Glob
---

# Initialize house style

Create the project's house-style config from the bundled template.

## Procedure
1. Check whether `${CLAUDE_PROJECT_DIR}/.prompt-optimizer/house-style.md` already exists.
   - If it exists, show its current contents and ask the user whether to overwrite. Stop unless they confirm.
2. Read the template: `${CLAUDE_PLUGIN_ROOT}/reference/house-style-template.md`.
3. Write it to `${CLAUDE_PROJECT_DIR}/.prompt-optimizer/house-style.md` (create the `.prompt-optimizer/` directory if needed).
4. Tell the user where it was written and that they should edit the sections to match the project, then re-run `/prompt-optimizer:optimize-prompt` or `/prompt-optimizer:scan-prompts`.
```

- [ ] **Step 2: Verify**

Run: `head -1 skills/init-house-style/SKILL.md` (expect `---`) and `grep -q "house-style.md" skills/init-house-style/SKILL.md`
Expected: exits 0.

- [ ] **Step 3: Commit**

```bash
git add skills/init-house-style/SKILL.md
git commit -m "feat: add init-house-style skill"
```

---

## Task 6: `scan-prompts` skill + `prompt-scanner` agent (mode B)

**Files:**
- Create: `skills/scan-prompts/SKILL.md`
- Create: `agents/prompt-scanner.md`

**Interfaces:**
- `scan-prompts` dispatches the `prompt-scanner` agent.
- `prompt-scanner` consumes `reference/best-practices.md` + house style; produces per-finding diffs applied only on approval, plus a final summary.

- [ ] **Step 1: Create `agents/prompt-scanner.md`**

```markdown
---
name: prompt-scanner
description: Discovers prompts embedded in a project's code/config and proposes best-practice and house-style improvements, applying edits only on explicit user approval.
tools: Read, Glob, Grep, Edit
---

You are the prompt-scanner. You find prompts embedded in this project and improve them.

## What counts as a prompt
- String literals/templates passed to an LLM API (system prompts, message content, instruction templates).
- Dedicated prompt files (e.g. `*.prompt`, `prompts/*.md`, `*.txt` used as prompts).
- Template strings with prompt-like content (role framing, task instructions, output-format directions).

## Procedure
1. Read the ruleset: `${CLAUDE_PLUGIN_ROOT}/reference/best-practices.md`.
2. Load house style: `${CLAUDE_PROJECT_DIR}/.prompt-optimizer/house-style.md` if present, else note it is absent and use defaults.
3. Discover candidates with Glob/Grep across the project: search for common LLM call sites (e.g. `system`, `messages`, `prompt`, `completion`, `ChatPromptTemplate`, `client.messages.create`, `anthropic`, `openai`) and prompt files. Read candidate files to confirm.
4. For EACH confirmed prompt, evaluate against every rule group, then present:
   - **Location:** `path:line`
   - **Issues:** rules violated (by name)
   - **Proposed rewrite:** show as a diff
   - **Rationale:** one line per rule applied
5. Ask the user to approve THIS change. Apply the edit with the Edit tool ONLY if they approve. Move to the next finding regardless.
6. After all findings, print a summary: total prompts found, changes applied, changes skipped, files touched.

## Rules of engagement
- Never edit a file without explicit per-change approval.
- Preserve runtime structure: keep variable interpolations/placeholders intact when rewriting.
- Do not change a prompt's meaning; standardize its form.
- If zero prompts are found, say so clearly and stop.
```

- [ ] **Step 2: Create `skills/scan-prompts/SKILL.md`**

```markdown
---
description: Scan the current project for prompts embedded in code/config and propose best-practice + house-style improvements (apply on approval). Use when the user wants to audit or standardize prompts across the codebase.
argument-hint: "optional path or glob to limit the scan"
---

# Scan project prompts

Dispatch the `prompt-scanner` subagent to audit and improve prompts across the project.

## Procedure
1. If `$ARGUMENTS` is provided, pass it to the subagent as the path/glob to limit the scan; otherwise scan the whole project.
2. Launch the `prompt-scanner` subagent (Task/Agent tool) with this instruction: "Scan {scope} for embedded prompts and propose best-practice + house-style improvements, applying edits only on my approval. Follow your agent instructions."
3. Run the subagent in the foreground so the user can approve changes interactively.
4. Relay the subagent's final summary to the user.
```

- [ ] **Step 3: Verify both files**

Run: `head -1 agents/prompt-scanner.md` (expect `---`); `grep -q "name: prompt-scanner" agents/prompt-scanner.md`; `head -1 skills/scan-prompts/SKILL.md` (expect `---`)
Expected: all exit 0.

- [ ] **Step 4: Commit**

```bash
git add agents/prompt-scanner.md skills/scan-prompts/SKILL.md
git commit -m "feat: add scan-prompts skill and prompt-scanner agent"
```

---

## Task 7: Test fixtures, sample project, and README

**Files:**
- Create: `tests/fixtures/optimize/01-vague-before.md`
- Create: `tests/fixtures/optimize/01-vague-after.md`
- Create: `tests/sample-project/app.py`
- Create: `tests/sample-project/README.md`
- Create: `README.md`

**Interfaces:**
- Produces: manual-review fixtures and a tiny project the scanner can be run against.

- [ ] **Step 1: Create `tests/fixtures/optimize/01-vague-before.md`**

```markdown
write a summary of the meeting notes and dont be too long
```

- [ ] **Step 2: Create `tests/fixtures/optimize/01-vague-after.md`** (the expected shape, for manual comparison)

```markdown
<role>You are a precise meeting-notes summarizer.</role>

<instructions>
Summarize the meeting notes provided below. Produce a summary of at most 5 sentences
that captures decisions, owners, and next steps.
</instructions>

<output_format>Flowing prose, no preamble.</output_format>

<meeting_notes>
{{MEETING_NOTES}}
</meeting_notes>
```

- [ ] **Step 3: Create `tests/sample-project/app.py`** (embedded prompt for the scanner to find)

```python
import anthropic

client = anthropic.Anthropic()

# An intentionally weak prompt for the scanner to improve.
SYSTEM = "you are a bot. answer questions. dont make mistakes."

def ask(question: str) -> str:
    msg = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=512,
        system=SYSTEM,
        messages=[{"role": "user", "content": question}],
    )
    return msg.content[0].text
```

- [ ] **Step 4: Create `tests/sample-project/README.md`**

```markdown
# Sample project (test fixture)

Run `/prompt-optimizer:scan-prompts` from this directory. The scanner should find
the `SYSTEM` prompt in `app.py` and propose a best-practice rewrite.
```

- [ ] **Step 5: Create `README.md`**

```markdown
# prompt-optimizer

A Claude Code plugin that optimizes and standardizes prompts against Claude's
prompt-engineering best practices plus your project's house style.

## Install (local dev)
```
claude --plugin-dir /path/to/prompt-optimizer
```

## Commands
- `/prompt-optimizer:optimize-prompt <prompt>` — rewrite a single/pasted prompt to best practices + house style. Non-destructive.
- `/prompt-optimizer:scan-prompts [path]` — find prompts embedded in your codebase and improve them (apply on approval).
- `/prompt-optimizer:init-house-style` — scaffold `.prompt-optimizer/house-style.md` into your project.

## How it works
The bundled ruleset (`reference/best-practices.md`) is distilled from Claude's
official prompting best practices and is the single source of truth. Your
project's `.prompt-optimizer/house-style.md` layers project conventions on top.

## Best-practices source
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
```

- [ ] **Step 6: Verify files exist**

Run: `ls tests/fixtures/optimize tests/sample-project README.md`
Expected: all listed, no errors.

- [ ] **Step 7: Commit**

```bash
git add tests README.md
git commit -m "test: add fixtures, sample project, and README"
```

---

## Task 8: Final validation

**Files:** none (validation only; fix-and-commit if issues found)

- [ ] **Step 1: Structural validation**

Run: `claude plugin validate .` if the CLI is available.
Fallback (always run): verify JSON parses, every `SKILL.md`/agent file starts with `---` frontmatter, and `${CLAUDE_PLUGIN_ROOT}/reference/best-practices.md` is referenced by both `optimize-prompt` and `prompt-scanner`.

Run (fallback):
```
node -e "JSON.parse(require('fs').readFileSync('.claude-plugin/plugin.json','utf8'));console.log('json ok')"
for f in skills/*/SKILL.md agents/*.md; do head -1 "$f" | grep -q '^---' && echo "fm ok: $f" || echo "FM MISSING: $f"; done
grep -l "reference/best-practices.md" skills/optimize-prompt/SKILL.md agents/prompt-scanner.md
```
Expected: `json ok`, `fm ok:` for every file, and both files listed by grep.

- [ ] **Step 2: Load check (if CLI available)**

Run: `claude --plugin-dir . -p "/help" ` or list plugins to confirm skills load. If CLI/headless run isn't possible, note it as a manual step for the user.

- [ ] **Step 3: Commit any fixes**

```bash
git add -A
git commit -m "chore: final validation fixes" || echo "nothing to fix"
```

---

## Self-Review (completed during planning)

- **Spec coverage:** §2 modes A/C → Task 4; mode B → Task 6; §4 ruleset → Task 2; §5 house style → Tasks 3+5; §7 bundled → Task 2 content; §8 testing → Tasks 7+8; §9 phasing → Tasks 1–5 (Phase 1), Task 6 (Phase 2); §10 distribution → README in Task 7. Phase 3 intentionally omitted.
- **Placeholder scan:** intentional `{{PLACEHOLDER}}`/`{{MEETING_NOTES}}` are output conventions, not plan gaps. No TODO/TBD.
- **Type consistency:** rule names (`set-role`, `xml-tags`, etc.) defined in Task 2 are the same names referenced by Tasks 4 and 6; file paths consistent across tasks.
```

