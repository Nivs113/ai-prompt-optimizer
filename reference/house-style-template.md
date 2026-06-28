# Prompt house style

This file defines project-specific prompt conventions layered ON TOP of Claude's
best practices. The optimizer applies best practices first, then enforces these.
House style may tighten or specialize defaults but must not override safety guidance.

Edit the sections below to match your project. Delete any you don't need.

## Tone & voice
- (e.g.) Direct, concise, no marketing language.

## Required prompt sections
List the sections every standardized prompt in this project should contain, in order.
- (e.g.) `<role>`, `<context>`, `<instructions>`, `<constraints>`, `<output_format>`

## Default output format
- (e.g.) Return JSON matching the documented schema; no prose preamble.

## Tag & naming conventions
- (e.g.) Use snake_case XML tag names; use `<example>` for samples.

## Forbidden patterns
- (e.g.) No "CRITICAL/MUST" pressure language; no prefilled assistant turns; no ellipses.

## Project glossary / domain notes
- (e.g.) Terms the model should use consistently.
