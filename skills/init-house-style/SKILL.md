---
description: Generate a ready-to-use prompt house-style config for the current project by inferring conventions from the codebase, docs, and this session — no manual template editing.
allowed-tools: Read, Glob, Grep, Write
---

# Initialize house style

Generate a concrete, **ready-to-use** `.prompt-optimizer/house-style.md` for THIS project. Infer real values from the project — do NOT emit a blank template with `(e.g.)` placeholders.

## Procedure

1. **Check for an existing config.** If `${CLAUDE_PROJECT_DIR}/.prompt-optimizer/house-style.md` already exists, show it and ask whether to regenerate. Stop unless the user confirms.

2. **Gather context** (read-only):
   - If `${CLAUDE_PROJECT_DIR}/.prompt-optimizer/project-index.md` exists, read it. Otherwise do a light scan: detect the language/stack and LLM SDKs, and locate existing prompts (system prompts, message templates, prompt files).
   - Read a few of the project's existing prompts to learn current conventions: Do they use XML tags? roles? few-shot examples? Are model outputs parsed as JSON/structured (→ structured output is the norm) or rendered as prose?
   - Read `README`/docs and the package manifest for domain, product voice, and glossary terms.
   - Fold in any preferences the user has expressed in the CURRENT conversation (e.g. tone, banned phrasing, output expectations).

3. **Infer concrete values** for every section below. Fill them with real, project-specific content — never `(e.g.)` placeholders. For genuinely subjective fields (default tone, default output format) where the project gives no clear signal, choose a sensible default consistent with the observed style and the best-practices ruleset, and note that it is an assumption.

   Produce the same section schema as `${CLAUDE_PLUGIN_ROOT}/reference/house-style-template.md`:
   - **Tone & voice** — derived from docs/prompts, else a sensible default.
   - **Required prompt sections** — the ordered sections prompts should contain, aligned to best practices (role, context, instructions, constraints, output_format) and to what the project's better prompts already do.
   - **Default output format** — JSON/structured if the code parses model output; otherwise prose. State which and why.
   - **Tag & naming conventions** — match the casing/tag style already used (snake_case vs camelCase).
   - **Forbidden patterns** — best-practice defaults (no CRITICAL/MUST pressure, no prefilled assistant turns, no ellipses) plus anything the codebase clearly avoids.
   - **Project glossary / domain notes** — real terms drawn from the project.

4. **Write** the filled-in file to `${CLAUDE_PROJECT_DIR}/.prompt-optimizer/house-style.md` (create `.prompt-optimizer/` if needed). Start the file with a one-line note that it was auto-generated and is safe to edit.

5. **Report** a short "what I inferred and why" summary. Explicitly flag the fields you had to ASSUME (the subjective ones) so the user can adjust just those. Tell them it is ready to use as-is and that `optimize-prompt` and `scan-prompts` will pick it up automatically.

## Rules of engagement
- Read-only except for writing the house-style file.
- Produce concrete values, not placeholders. If you genuinely cannot infer a field, state your assumption inline rather than leaving a blank.
- Keep it concise — a usable convention sheet, not an essay.
- House style may tighten best-practice defaults but must never override safety guidance.
