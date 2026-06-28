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
- `/prompt-optimizer:index-project` — cache a `.prompt-optimizer/project-index.md` (stack, LLM SDKs, prompt locations, conventions) that the optimizer and scanner reuse for faster, more tailored suggestions.
- `/prompt-optimizer:refresh-best-practices` — re-fetch Claude's live prompting docs and regenerate the bundled ruleset, preserving rule names.

## How it works
The bundled ruleset (`reference/best-practices.md`) is distilled from Claude's
official prompting best practices and is the single source of truth. Your
project's `.prompt-optimizer/house-style.md` layers project conventions on top.
Run `/prompt-optimizer:index-project` once to cache project context; both the
optimizer and scanner read it automatically when present, and fall back to a
live light-scan when absent. Run `/prompt-optimizer:refresh-best-practices` to
keep the ruleset current with the live docs.

## Best-practices source
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
