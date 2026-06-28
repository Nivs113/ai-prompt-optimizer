---
description: Refresh the bundled best-practices ruleset by re-fetching Claude's live prompt-engineering docs and re-distilling them. Use when Claude's prompting guidance may have changed or the ruleset looks stale.
allowed-tools: WebFetch, Read, Write
---

# Refresh best practices

Regenerate `${CLAUDE_PLUGIN_ROOT}/reference/best-practices.md` from the live source.

## Source
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices

## Procedure
1. Read the current ruleset at `${CLAUDE_PLUGIN_ROOT}/reference/best-practices.md` and note the existing group headings and rule slugs (the `**rule-slug**:` names).
2. WebFetch the source URL. Extract every best-practice technique and its concrete rule.
3. Re-distill into the SAME format as the current file:
   - Top matter: title, a `Source:` line, a `Distilled:` line with today's date (ask the user for today's date if you are unsure), and the "applies to current models / model-specific notes are labelled" line.
   - `## N. <Group>` headings, numbered.
   - `- **rule-slug**: one-line rule.` bullets.
4. PRESERVE existing rule slugs wherever the rule still exists, so references in `optimize-prompt` and `prompt-scanner` stay valid. Add new slugs only for genuinely new guidance; remove a slug only if the guidance is gone from the source.
5. Write the regenerated content back to `${CLAUDE_PLUGIN_ROOT}/reference/best-practices.md`.
6. Report a summary: groups/rules added, changed, and removed. If any removed slug is still referenced by `optimize-prompt` or `prompt-scanner`, flag it explicitly so the user can update those references.

## Rules of engagement
- Keep the named-rule + grouped structure intact; downstream skills depend on it.
- Do not invent rules that are not present in the source.
- If the fetch fails, leave the existing file unchanged and tell the user.
