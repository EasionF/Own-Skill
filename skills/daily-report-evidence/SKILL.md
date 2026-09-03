---
name: daily-report-evidence
description: Gather and reconcile evidence for a Chinese work daily report. Use when Codex needs to draft or verify a daily report from multiple local sources such as the current thread, the user-confirmed workspace root, the current machine's download directory, browser history, or local tool records. Use this before filling a report form, and use it whenever the report must be based on evidence instead of guesswork.
---

# Daily Report Evidence

Use this skill to build a report from evidence, not memory.

## Workflow

1. Collect same-day evidence from the highest-value sources first:
   - current thread
   - `<WORKSPACE_ROOT>` work-related file changes
   - `%USERPROFILE%\Downloads` work-related files
   - Chrome and Edge same-day browsing history
   - local tool traces such as `%USERPROFILE%\.codex`
2. Remove noise:
   - ignore cache, `__pycache__`, binaries, and generated files unless they prove a meaningful action
   - do not count non-work browsing or unrelated downloads
3. Cross-check:
   - browsing history alone is not enough
   - logs alone are not enough
   - prefer conclusions supported by at least two sources when possible
4. Mark uncertainty early:
   - if the main task, completion boundary, or ownership is unclear, ask the user
   - do not infer achievements from weak signals
5. Produce the report in this fixed structure:
   - 今日完成工作
   - 未完成工作
   - 未完成原因
   - 需协调工作
   - 今日学习内容

## Output Rules

- Write in Chinese.
- Keep the tone pragmatic, readable, and slightly polished.
- Do not sound stiff or theatrical.
- If a section is truly empty, write `无` and explain why.
- Distinguish clearly between:
  - completed work
  - ongoing work
  - blockers
  - learning/research

## Evidence Heuristics

- `<WORKSPACE_ROOT>`:
  treat edited scripts, config files, tests, logs, and generated outputs as candidate evidence; ignore pure bytecode churn unless it supports a real task.
- `%USERPROFILE%\Downloads`:
  treat same-day installers, docs, exports, or recovery files as hints; only include them if they relate to a real task.
- Browser history:
  use it to support learning, investigation, model selection, bug fixing, or product research; do not convert every search into “completed work”.
- Local tool traces:
  use them to confirm what was worked on, not to fabricate outcomes.

## Handoff

- If the user wants text only, output a complete daily report draft.
- If the user wants the form filled, hand the confirmed content to `computer-use`.
- If browser evidence is needed, use `browser-use` first and only bring back the work-related subset.
