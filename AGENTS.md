Before making any code changes to this project, you MUST first consult the NeoForge documentation for the relevant Minecraft version (26.1.2):

1. **NeoForge Documentation** — https://github.com/neoforged/Documentation.git
   Fetch the relevant `.md` file from `docs/` tree for the API you're working with (e.g. `docs/items/index.md` for items, `docs/concepts/registries.md` for registries).

Do NOT guess API signatures, package paths, or class names. Always verify against the docs first. If the docs don't cover the exact case, look at decompiled vanilla sources in the Gradle cache matching this MC version.


# NovaDyne working agreement

## Scope and machine limits
- Respond in Brazilian Portuguese, plainly and concisely.
- This is nicotfpn/Novadyne-MOD. Check current branch, HEAD and dirty files at task start.
- The user's Windows PC has 4 GB RAM and limited free disk. Never start Gradle,
  Minecraft, Java language servers, Docker, WSL installation, package installation
  or large dependency downloads without explicit approval for that action.
- Work on one bounded outcome per request. Preserve existing world data, registry
  IDs, recipes and unrelated behavior unless the requested change requires otherwise.
- Do not overwrite unrelated user changes. Never discard work to make a test pass.

## Git and approvals
- Local edits required by an implementation request are authorized. Read-only requests
  authorize no edits. Explain the intended behavior before editing.
- No commit, push, merge, PR creation, release, remote branch changes or CI dispatch
  without explicit user approval. Keep the prepared diff reviewable locally.
- Never force-push, hard-reset or delete branches/files to resolve routine problems.
- Permissions in opencode.json supplement these instructions; they are not a security
  sandbox. Do not bypass approval by shell quoting, aliases, scripts, APIs or tools.
- When remote writes are approved, submit only the reviewed task's changes. Include
  the status update in that same approved submission; do not silently publish it.

## Context and handoff
- At start read docs/STATUS.md (at most about 100 lines) and verify its reference
  against current files. The repository is authoritative; the status is a checkpoint.
- Inspect only files relevant to the task. Use targeted searches and short log excerpts.
  Do not repeat a whole-repository audit for every request.
- Keep decisions and exact test evidence in docs/STATUS.md after implementation tasks.
  Record local-only, committed, pushed and merged separately. Do not imply remote sync.
- Automatic compaction is enabled. Before losing context, preserve objectives,
  decisions, edited paths, test results and next action. Never rely on chat alone.
- Do not claim unlimited context, free quotas, automatic new primary chats or remote
  builds without access/approval. If unavailable, state the exact missing capability.

## Implementation and independent review
- Primary agent implements; use novadyne-review once after meaningful code changes,
  sequentially. Give it the objective, exact changed files/diff and test evidence.
- No parallel writers. No recursive delegation. For a trivial doc fix, skip review.
- Reviewer must inspect actual code independently, report file/method and reproduction,
  and separate confirmed code findings from hypotheses and untested behavior.
- Correct material findings, then repeat only affected checks. Stop expanding scope.

## Technical focus
- Validate inventory slots at the BlockEntity/capability layer, not only in menus.
  Check shift-click routing, sided insertion/extraction and crafting remainders.
- Energy: preserve INTERNAL/EXTERNAL boundaries and transaction rollback. Check
  conservation, blocked targets, multiple consumers and zero/partial transfers.
- Fluids: preserve water-only input, tank bounds, rollback and per-cycle consumption.
- Side modes are relative to front; test all horizontal orientations and persistence.
- Recipe identity must agree with progress; changing recipe must not reuse old work.
- Existing machine processing is Java-based. Avoid unrequested recipe-system rewrites.
- Prefer focused regression GameTests for behavior changes; don't launch them locally
  without approval. GitHub Actions requires an approved push/PR; it is not automatic
  from local edits and must not be described as run before evidence is available.
- Never label a static inspection as a successful runtime test. Finish with changes,
  checks actually run, checks pending and a short visual test for the 4 GB PC.
