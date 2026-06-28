---
description: Build a cached index of how this project uses prompts (LLM SDKs, prompt files, conventions) so the optimizer and scanner give faster, more tailored suggestions.
allowed-tools: Read, Glob, Grep, Write
---

# Index project prompt-context

Scan the project once and cache a context index the other skills can reuse.

## Procedure
1. Detect LLM SDKs / frameworks in use: grep source and dependency manifests (package.json, requirements.txt, pyproject.toml, go.mod, Gemfile, etc.) for `anthropic`, `@anthropic-ai`, `openai`, `langchain`, `llamaindex`, `google.generativeai`, `genai`, `cohere`, `ollama`, `mistralai`.
2. Locate prompt material: prompt files/dirs (`prompts/`, `*.prompt`, `*.prompt.md`) and LLM call sites (`messages.create`, `system=`, `system:`, `ChatPromptTemplate`, `completion`). Record file paths and line numbers for call sites.
3. Infer existing conventions: dominant language/stack, and whether prompts already use XML tags, roles, examples, and where prompts tend to live.
4. Write the index to `${CLAUDE_PROJECT_DIR}/.prompt-optimizer/project-index.md` (create `.prompt-optimizer/` if needed) with these sections:
   - `## Stack` — languages, frameworks.
   - `## LLM SDKs` — detected SDKs and where they are used.
   - `## Prompt locations` — files and call sites as `path:line`.
   - `## Observed conventions` — what the project already does well / inconsistently.
   - `## Generated` — today's date (ask the user if unsure).
5. Tell the user the index was written and that `optimize-prompt` and `scan-prompts` will use it automatically.

## Rules of engagement
- Read-only except for writing the index file.
- Keep the index concise; it is a map, not a copy of the code.
- If nothing prompt-related is found, write an index that says so, and tell the user.
