# Claude Prompt-Engineering Best Practices (distilled)

Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
Distilled: 2026-06-28. Applies to current Claude models (Fable 5, Opus 4.8, Sonnet 4.6, Haiku 4.5). Model-specific notes are labelled.

When optimizing a prompt, evaluate it against every rule below. For each change, cite the rule name in the rationale.

## 1. Clarity & directness
- **be-explicit**: Give clear, specific instructions; treat Claude as a capable new hire lacking your context. State desired output and constraints exactly.
- **request-above-and-beyond**: If you want fully-featured output, ask for it explicitly (e.g. "Include as many relevant features as possible") rather than relying on inference.
- **sequential-steps**: When order/completeness matters, give steps as a numbered or bulleted list.
- **colleague-test**: A prompt a low-context colleague would find confusing will confuse Claude too.

## 2. Context & motivation
- **explain-why**: State the motivation behind an instruction; Claude generalizes from the explanation (e.g. "...read aloud by TTS, so never use ellipses").

## 3. Examples (few-shot / multishot)
- **use-examples**: Add 3–5 examples to steer format, tone, structure.
- **examples-relevant-diverse**: Make examples mirror the real use case and cover edge cases without leaking unintended patterns.
- **examples-tagged**: Wrap each example in `<example>` tags (`<examples>` around the set).

## 4. XML structure
- **xml-tags**: Wrap distinct content types in their own descriptive tags (`<instructions>`, `<context>`, `<input>`).
- **xml-consistent-nested**: Use consistent tag names; nest tags for natural hierarchy.

## 5. Role / system prompt
- **set-role**: Set a role in the system prompt to focus tone and behavior; even one sentence helps.

## 6. Long-context handling (20k+ tokens)
- **data-on-top**: Put long documents/inputs near the top, above the query and instructions.
- **query-at-bottom**: Place the actual question/instructions after the data (can improve quality up to ~30%).
- **document-metadata-tags**: Wrap each document in `<document>` with `<source>` and `<document_content>` subtags.
- **ground-in-quotes**: For long-document tasks, ask Claude to extract relevant quotes first (in `<quotes>` tags) before answering.

## 7. Output & formatting
- **say-what-to-do**: Tell Claude what to do, not what to avoid ("write flowing prose" beats "don't use markdown").
- **xml-format-indicators**: Use tags like `<smoothly_flowing_prose_paragraphs>` to mark desired output shape.
- **match-prompt-style**: Match the prompt's own formatting to the desired output style.
- **explicit-format-guidance**: For strict formatting, give detailed explicit guidance.
- **prefer-structured-outputs**: Don't rely on prefill (deprecated on 4.6+); use Structured Outputs / tool enums for schemas and "respond without preamble" to drop preambles.

## 8. Tool use
- **explicit-action**: To make Claude act (not just suggest), use imperative phrasing ("Change this function", not "Can you suggest changes").
- **avoid-over-prompting**: Don't use "CRITICAL/MUST" pressure; modern models overtrigger. Use normal phrasing ("Use this tool when...").
- **parallel-tool-calls**: Encourage parallel independent tool calls; require sequential only for dependent calls.

## 9. Thinking & reasoning
- **calibrate-thoroughness**: Replace blanket "always use X" with targeted "use X when it helps"; remove anti-laziness over-prompting.
- **adaptive-thinking**: Prefer adaptive thinking; control depth via `effort`, not `budget_tokens` (deprecated/400 on newer models).
- **self-check**: Ask Claude to verify its answer against criteria before finishing.
- **cot-fallback-tags**: When thinking is off, request step-by-step reasoning using `<thinking>` and `<answer>` tags. Note: on Opus 4.5 with thinking off, prefer "consider/evaluate/reason through" over "think".

## 10. Agentic safety & quality
- **confirm-destructive**: Instruct confirmation before destructive/irreversible/shared-system actions; never bypass safety checks as a shortcut.
- **avoid-overengineering**: Keep solutions minimal; no unrequested features, abstractions, defensive code, or docs.
- **no-test-hardcoding**: Solve the general problem, not just the test cases; report bad/infeasible tests instead of working around them.
- **investigate-before-answering**: Never speculate about unopened code; read referenced files before answering.
- **state-tracking** (long-horizon): Use structured files (e.g. `tests.json`) for state, freeform notes for progress, git for checkpoints; emphasize incremental progress.
