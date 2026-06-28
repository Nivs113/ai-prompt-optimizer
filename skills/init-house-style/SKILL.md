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
