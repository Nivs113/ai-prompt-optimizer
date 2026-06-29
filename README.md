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
