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
