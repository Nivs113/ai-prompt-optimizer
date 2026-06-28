# Design: `prompt-optimizer` Claude Code plugin

**Date:** 2026-06-28
**Status:** Approved (design); pending implementation plan

## 1. Purpose

A shareable Claude Code plugin that optimizes and standardizes prompts against
**Claude's documented prompt-engineering best practices plus a project-specific
house style**. It is project-context-aware: it tailors suggestions to the
project it is run in rather than applying generic rules blindly.

Source of best practices:
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
(bundled as a distilled ruleset; see §7).

## 2. Scope

Three usage modes, collapsed into two front-ends over one shared engine:

- **A. Prompts the user writes *to* Claude Code** and **C. any prompt the user
  pastes in** → a single **interactive optimizer**. The only difference between
  A and C is whether project context is auto-loaded.
- **B. Prompts embedded *in the project's application code*** (system prompts,
  message templates, prompt files) → a **project scanner** that discovers them
  and proposes improvements with **suggest + apply on approval**.

Out of scope (for now): optimizing prompts for non-Claude models; automatic
unattended rewriting of files; an MCP server (considered and rejected as
overkill — see §11).

## 3. Architecture — one engine, thin front-ends

```
prompt-optimizer/
├── .claude-plugin/
│   └── plugin.json                   # manifest (only `name` required)
├── skills/
│   ├── optimize-prompt/
│   │   └── SKILL.md                  # interactive optimizer (modes A + C)
│   ├── scan-prompts/
│   │   └── SKILL.md                  # entry point for mode B; dispatches the subagent
│   └── init-house-style/
│       └── SKILL.md                  # scaffolds the house-style config into a project
├── agents/
│   └── prompt-scanner.md             # subagent: discover prompts -> evaluate -> propose diffs
└── reference/
    ├── best-practices.md             # THE distilled ruleset (single source of truth)
    └── house-style-template.md       # default / example house style
```

Key structural facts (verified against current Claude Code plugin docs):

- The manifest lives **only** at `.claude-plugin/plugin.json`; everything else
  lives at the plugin root.
- **Skills are the slash-command mechanism.** A skill in `skills/<name>/SKILL.md`
  is invoked as `/prompt-optimizer:<name>` and can also be auto-invoked by the
  model. No separate `commands/` directory is needed.
- Bundled files are referenced via the `${CLAUDE_PLUGIN_ROOT}` variable; the
  project root is `${CLAUDE_PROJECT_DIR}`.

Design principles:

- **Single source of truth:** `reference/best-practices.md` is the one ruleset.
  Both `optimize-prompt` and the `prompt-scanner` agent read it, so the rules
  never diverge between modes.
- **Context isolation:** the scanner runs as a **subagent** so heavy,
  whole-project discovery does not pollute the user's main chat context.
- **Small, focused units:** each skill/agent has one clear job and a documented
  input/output.

## 4. The best-practices ruleset

`reference/best-practices.md` is a named checklist distilled from the official
doc, grouped the way the doc is. Each rule has a stable name so the optimizer can
cite *which* rule drove each change. Rule groups:

1. **Clarity & directness** — explicit, specific instructions; request
   "above and beyond" explicitly; sequential numbered steps when order matters.
2. **Context / motivation** — explain *why* an instruction matters so the model
   generalizes correctly.
3. **Few-shot examples** — 3–5 examples, relevant + diverse, wrapped in
   `<example>` / `<examples>` tags.
4. **XML structure** — wrap distinct content types in consistent, descriptive
   tags (`<instructions>`, `<context>`, `<input>`); nest for hierarchy.
5. **Role / system prompt** — set a role in the system prompt to focus tone and
   behavior.
6. **Long-context ordering** — longform data near the top, query/instructions at
   the bottom; structure documents with `<document>` metadata tags; ground
   answers in quotes for long-document tasks.
7. **Output & formatting** — say what *to* do rather than what not to do; use XML
   format indicators; match prompt style to desired output; give explicit
   formatting guidance; prefer structured outputs over (now-deprecated) prefill.
8. **Tool-use triggering** — be explicit when action (not just suggestion) is
   wanted; avoid over-prompting ("CRITICAL/MUST") which now overtriggers; use
   parallel tool-call guidance when appropriate.
9. **Thinking & reasoning** — calibrate thoroughness (avoid over/under
   prompting); use adaptive thinking; ask the model to self-check; use
   `<thinking>`/`<answer>` tags for manual chain-of-thought fallback.
10. **Agentic safety & quality** — confirm before destructive/irreversible
    actions; avoid overengineering; avoid hard-coding to tests; investigate
    before answering (anti-hallucination).

The ruleset cites the source URL and notes that some guidance is model-specific
(e.g. Fable 5, Opus 4.8); model-specific notes are kept light and clearly
labelled so the ruleset stays usable across models.

## 5. House style (the user's layer)

- A markdown file in the user's project: **`.prompt-optimizer/house-style.md`**.
- Injected into the engine alongside the ruleset; the house style takes
  precedence where it conflicts with a default-level best-practice preference
  (it cannot override safety guidance).
- `init-house-style` scaffolds it from `reference/house-style-template.md`.
- If the file is absent, the engine falls back to the bundled template and offers
  to create the project file.
- **Format decision:** markdown (not YAML) — easier for both the user to write
  and the model to consume; the template documents the expected sections (tone,
  required prompt sections, default output format, forbidden patterns).

## 6. Behaviors

### 6.1 Interactive optimizer — `optimize-prompt` (modes A + C)

Input: a prompt supplied as `$ARGUMENTS` or pasted into the conversation.

Steps:
1. Load `reference/best-practices.md` and the project house style (if present).
2. If running inside a project, gather light project context (stack, conventions,
   relevant existing prompts) to tailor suggestions; skip for a bare pasted prompt.
3. Produce, non-destructively:
   - **(1)** the rewritten prompt in a copy-ready code block,
   - **(2)** a short rationale naming the rules applied,
   - **(3)** a brief checklist of issues found / fixed.

### 6.2 Project scanner — `scan-prompts` + `prompt-scanner` agent (mode B)

`scan-prompts` is a thin skill that dispatches the `prompt-scanner` subagent.

The subagent:
1. Discovers prompt-like strings across the project (system prompts, message
   templates, dedicated prompt files), language-agnostically via heuristics +
   reading candidate files.
2. Evaluates each against the ruleset + house style.
3. For each finding, presents: the location, the suggested rewrite as a diff, and
   a rationale.
4. **Applies the edit only on explicit user approval, one change at a time.**
   Never edits without confirmation.
5. Emits a final summary of findings, applied changes, and skipped items.

## 7. Best-practices source: bundled

Ship the distilled ruleset inside the plugin: offline, fast, version-pinned, and
deterministic across runs. The ruleset records the source URL and the date it was
distilled. A "refresh from the live doc" capability is **deferred to Phase 3**
(optional) rather than fetched at runtime on every use.

## 8. Testing & verification

- **Structural:** `claude plugin validate ./prompt-optimizer`.
- **Load:** `claude --plugin-dir ./prompt-optimizer` to confirm skills/agent load
  and are invocable.
- **Functional fixtures:** a `tests/` (or `examples/`) folder containing
  before/after fixture prompts for the optimizer, and a tiny sample project with
  embedded prompts to confirm the scanner discovers and rewrites them correctly.
- Because outputs are non-deterministic, functional checks are manual/spot review
  of fixtures rather than exact-match assertions.

## 9. Build order (incremental)

- **Phase 1:** `plugin.json` + `reference/best-practices.md` +
  `reference/house-style-template.md` + `optimize-prompt` skill +
  `init-house-style` skill. Delivers modes A + C.
- **Phase 2:** `scan-prompts` skill + `prompt-scanner` agent. Delivers mode B.
- **Phase 3 (implemented 2026-06-28):** `refresh-best-practices` skill (WebFetch +
  re-distill, preserving rule slugs) and `index-project` skill (cached
  `.prompt-optimizer/project-index.md` consumed by `optimize-prompt` and
  `prompt-scanner`).

## 10. Distribution

- Local development: `claude --plugin-dir ./prompt-optimizer`.
- Later sharing: add a `marketplace.json` so others can
  `claude plugin install`. Not required for initial use.

## 11. Alternatives considered

- **Lean (single skill + one command):** rejected — clumsy scanning, pollutes
  main context.
- **MCP-server-backed:** rejected — much heavier to build/maintain; only worth it
  if the optimizer must be callable from tools outside Claude Code, which is not a
  requirement.

## 12. Open items / future

- ~~Phase 3 "refresh from live doc" mechanism (script vs skill)~~ — RESOLVED:
  skill-based (`refresh-best-practices`), implemented 2026-06-28.
- ~~Richer project-context indexing for the scanner~~ — RESOLVED: `index-project`
  skill with a cached index, implemented 2026-06-28.
- ~~Project is not yet a git repository~~ — RESOLVED: `git init` done; spec,
  plan, and plugin committed.
- ~~Optional `marketplace.json` for `claude plugin install` distribution~~ —
  RESOLVED: `.claude-plugin/marketplace.json` added (marketplace `nirav-plugins`,
  plugin `source: "./"`), implemented 2026-06-28.
