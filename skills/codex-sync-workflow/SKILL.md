---
name: codex-sync-workflow
description: Use when the user explicitly asks to sync another Codex, perform dual-machine Codex sync, or work with the shared `codex-config` repository. This skill orchestrates the full workflow: read the shared repo docs, pull the latest changes, sync portable assets into the local `.codex` directory, recover new portable assets back into the repository, and handle Git commit/push steps while preserving local runtime state.
---

# Codex Sync Workflow

Use this skill only when the user explicitly mentions cross-machine Codex sync, syncing another machine, or the shared `codex-config` repository.

## Goal

Keep two Windows Codex environments aligned through the shared `codex-config` repository, while treating runtime state as local-only.

## Required References

Before making changes, read these files from the repository:

1. `<WORKSPACE_ROOT>\projects\codex-config\docs\SYNC_GUIDE.md`
2. `<WORKSPACE_ROOT>\projects\codex-config\docs\CONFLICT_RULES.md`
3. `<WORKSPACE_ROOT>\projects\codex-config\inventory\codex-assets-manifest.md`
4. `<WORKSPACE_ROOT>\projects\codex-config\docs\MACHINE_ONBOARDING.md` when the task is first-time setup on a machine

Do not restate those files from memory if they have changed. Re-read them.

## Trigger Scope

Valid examples:

- “同步另一台 Codex”
- “双机同步”
- “按 codex-config 仓库同步”
- “把这台机器的 skill 回收到共享仓库”
- “从 codex-config 拉最新并同步本机”

Do not trigger this skill for ordinary repository work, normal coding tasks, or unrelated Git usage.

## Workflow

1. Identify the direction of work:
   - repository to local machine sync
   - local machine recovery back into repository
   - bidirectional sync with Git pull, merge, and push
   - first-time onboarding for another machine
2. Confirm the workspace root for the current machine with the user, then inspect the local shared repository at `<WORKSPACE_ROOT>\projects\codex-config`.
3. If the task touches shared assets, run `git pull` first unless the user explicitly says not to.
4. Use the manifest as the source of truth for what is portable:
   - global `AGENTS.md`
   - listed user-maintained skills
   - templates
   - config template fragments
   - repository docs and manifests
5. Sync only the portable assets between:
   - repository root: `<WORKSPACE_ROOT>\projects\codex-config`
   - local Codex root: `%USERPROFILE%\.codex`
6. If the machine has a new portable skill or rule that is missing from the repository, recover it into the repository first.
7. If shared assets changed, stage, commit, and push them back through Git.
8. Report what changed locally, what changed in the repository, and any unresolved conflicts.

## Git Rules

Use Git as the transport for incremental shared changes.

Normal order:

1. `git pull`
2. modify or recover shared assets
3. `git add .`
4. `git commit -m "..."`
5. `git push`

When both machines changed the same asset:

- follow `docs\CONFLICT_RULES.md`
- merge intentionally
- do not overwrite blindly

## Local Sync Rules

Portable assets may be copied or merged into `%USERPROFILE%\.codex` when the task requires local activation.

Portable targets include:

- `%USERPROFILE%\.codex\AGENTS.md`
- `%USERPROFILE%\.codex\skills\`

Do not touch local-only runtime state:

- `auth.json`
- `sessions\`
- `cache\`
- `sqlite\`
- `logs_*.sqlite*`
- `state_*.sqlite*`
- `.tmp\`
- `plugins\cache\`
- bundled `.system` skills unless the user explicitly reclassifies them

## Recovery Rules

When recovering new shared capability from a machine:

1. decide whether the asset is truly portable and user-maintained
2. if yes, add it into `<WORKSPACE_ROOT>\projects\codex-config`
3. update the manifest if the shared skill set changed
4. commit and push so the other machine can inherit it

Do not recover:

- temporary experiments
- machine-specific trust entries
- auth or runtime files
- generated marketplace payloads

## Reporting

At the end of the workflow, report:

- whether the repository was pulled
- whether local `.codex` was updated
- whether new shared assets were recovered
- whether a commit and push happened
- any conflicts or skipped items

## Escalation

Stop and ask the user before continuing if:

- the shared repository is missing
- Git reports a conflict that cannot be resolved from repository docs
- a local skill appears important but its origin or ownership is unclear
- the workspace root for the current machine has not been confirmed yet
