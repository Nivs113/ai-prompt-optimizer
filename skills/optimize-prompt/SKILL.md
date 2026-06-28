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
3. Load project context (only when it helps tailor the prompt; skip entirely for a generic pasted prompt):
   - If `${CLAUDE_PROJECT_DIR}/.prompt-optimizer/project-index.md` exists, read it for fast project context (stack, SDKs, conventions, prompt locations).
   - Otherwise, if you are inside a project with source files, gather LIGHT context: detect the stack/conventions and, if the prompt references project concepts, skim the most relevant file(s). Do not do a full scan. You may suggest the user run `/prompt-optimizer:index-project` to cache this context for faster future runs.
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
