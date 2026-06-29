# prompt-optimizer

**A Claude Code plugin that rewrites your prompts to Claude's official best practices — and your project's house style.**

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-8A2BE2) ![version](https://img.shields.io/badge/version-0.2.0-blue)

Stop hand-tuning prompts. `prompt-optimizer` bakes in **44 named rules** distilled from Claude's [prompt-engineering docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) and applies them — to a prompt you paste, to prompts buried in your codebase, or to the instructions you give Claude Code itself. Every change is cited by rule, so you learn *why*.

## See it in action

Hand it a throwaway prompt:

```
write a summary of these meeting notes and dont be too long
```

Get back a structured, best-practice rewrite:

```xml
<role>You are a concise meeting summarizer.</role>

<meeting_notes>
{{PASTE_MEETING_NOTES_HERE}}
</meeting_notes>

<instructions>
Summarize the meeting notes above. Cover the key decisions, action items,
and any owners or deadlines mentioned.
</instructions>

<constraints>
- Write no more than 150 words.
- Use plain, direct language — no filler.
</constraints>

<output_format>
A short paragraph followed by a bullet list of action items (if any).
</output_format>
```

> **Why it changed:** added a role (`set-role`), wrapped each part in XML tags (`xml-tags`), moved the data above the task (`data-on-top`), turned *"dont be too long"* into a concrete limit (`say-what-to-do`), and pinned down the output shape (`explicit-format-guidance`).

## Install

```
/plugin marketplace add Nivs113/ai-prompt-optimizer
/plugin install prompt-optimizer@nirav-plugins
```

## Getting started in a project

After installing, do a quick one-time setup per project, then use it day to day.

**1. Create your house style** *(one-time)*

```
/prompt-optimizer:init-house-style
```

Auto-generates a ready-to-use `.prompt-optimizer/house-style.md` by inferring your project's conventions (tone, prompt structure, output format, naming, glossary) from the codebase, docs, and this session — no blank template to fill in. Review the short summary, tweak anything it flagged as an assumption, and **commit the file** as a shared team convention.

**2. Index the project** *(one-time; re-run when the stack changes)*

```
/prompt-optimizer:index-project
```

Caches `.prompt-optimizer/project-index.md` (stack, LLM SDKs, prompt locations). The optimizer and scanner read it automatically for faster, more tailored suggestions. It's a regenerable cache — safe to `.gitignore`.

**3. Use it** *(day to day)*

```
# polish a single prompt
/prompt-optimizer:optimize-prompt write a system prompt for a support bot

# audit & standardize prompts across the codebase — you approve each edit
/prompt-optimizer:scan-prompts
```

**4. Keep the rules current** *(occasional)*

```
/prompt-optimizer:refresh-best-practices
```

Re-fetches Claude's live docs and regenerates the bundled ruleset.

> Steps 1–2 are optional: the plugin still works without them (it falls back to sensible defaults and a quick live scan), but they make results sharper and consistent with your project.

## Commands

| Command | What it does |
|---|---|
| `/prompt-optimizer:optimize-prompt <prompt>` | Rewrite a pasted/typed prompt to best practices + house style. Non-destructive — returns text only. |
| `/prompt-optimizer:scan-prompts [path]` | Find prompts embedded in your codebase and improve them — **applies edits only on your per-change approval.** |
| `/prompt-optimizer:init-house-style` | Scaffold `.prompt-optimizer/house-style.md` for project-specific conventions. |
| `/prompt-optimizer:index-project` | Cache a project map (stack, LLM SDKs, prompt locations) so suggestions are faster and tailored. |
| `/prompt-optimizer:refresh-best-practices` | Re-fetch Claude's live docs and regenerate the bundled ruleset, preserving rule names. |

## How it works

- **One ruleset, one source of truth.** `reference/best-practices.md` is distilled from Claude's official prompting docs — 44 named rules across 11 groups (clarity, examples, XML structure, roles, long-context, output, tool use, thinking, agentic safety, capability-specific). Every suggestion cites the rule it applies.
- **Your house style on top.** `.prompt-optimizer/house-style.md` layers project conventions over the defaults. It can tighten them, but never overrides safety guidance.
- **Context-aware.** Run `index-project` once and both the optimizer and scanner reuse the cached map; otherwise they fall back to a quick live scan.
- **Safe by default.** The scanner never edits a file without your explicit approval.

## Updating

Bump the version in `.claude-plugin/plugin.json` **and** `.claude-plugin/marketplace.json`, push, then have users run:

```
/plugin marketplace update nirav-plugins
```

## Source

Best practices distilled from Claude's [prompt-engineering best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices). Refresh anytime with `/prompt-optimizer:refresh-best-practices`.

## License

[MIT](LICENSE) © Nirav Sangani
