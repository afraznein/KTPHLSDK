---
name: cpp-dev
description: Use BEFORE modifying any header in this repo (engine/eiface.h primarily) — the ABI append-only contract, the pfnClientCvarChanged trigger-scope fact, and the coordinated-bump workflow with KTPAMXX/KTP-ReHLDS.
---

# KTPhlsdk Development

This is the header-only Half-Life SDK fork that KTPAMXX and KTP-ReHLDS build
against, feeding a 24-instance production fleet. It has no binary of its own —
every change here is really the first step of a downstream KTPAMXX/KTP-ReHLDS
change, and inherits that risk.

## Hard safety rules
- **NEVER restart game servers** without the operator's explicit permission in
  the current conversation — even though this repo doesn't deploy directly,
  a header change forces a consumer rebuild that eventually does.
- Consumer binaries deploy as `.new` files and swap at the 03:00 ET nightly
  restart. Run the `ktp-code-review` agent on any nontrivial consumer rebuild
  before staging it, and md5-verify the result on all 24 instances — check
  `/tmp` for cores (`find /tmp -maxdepth 1 -name 'core.*' -mtime -1`), never
  the game trees (that search matches only `core.so`/`core.ini`/`core.wav` and
  always looks clean).
- Version bump = source version + CHANGELOG.md + README, done together, for
  this repo AND for any consumer whose ABI-visible header it touched.

## Repo-specific invariants
- The entire KTP delta is 9 lines in `engine/eiface.h`: one appended pointer,
  `pfnClientCvarChanged`, after `pfnCvarValue2` in `NEW_DLL_FUNCTIONS`.
  Everything else (`dlls/`, `cl_dll/`, `game_shared/`, `common/`, `public/`,
  every other `engine/` header) is 100% upstream-inherited — out of scope for
  cleanup, refactor, or style, even if it looks dated.
- Find the KTP delta boundary via git log, not by reading files: KTP-era
  commits are `1497c68` (the code change) plus `b7025fd`/`d68e0b6`/`e963857`
  (docs only).
- The struct-append is deliberate and load-bearing: `NEW_DLL_FUNCTIONS` grew by
  one pointer without bumping `NEW_DLL_FUNCTIONS_VERSION` (still `1`) — this is
  what keeps the ABI compatible for binaries still built against stock
  headers, on the assumption that KTP-ReHLDS never reads the new slot from an
  old-sized table. Don't "fix" the version number without auditing every
  consumer's version-gate logic first.
- `pfnClientCvarChanged` fires **only** from the `clc_cvarvalue2` query-response
  path in KTP-ReHLDS (`sv_user.cpp`, immediately after `pfnCvarValue2` in the
  same parse) — it is not unsolicited/continuous change detection, and
  consumers still need their own periodic `query_client_cvar` polling for real
  enforcement. README.md and the `eiface.h` doc comment currently overstate
  this ("fires for ANY cvar change", "without periodic polling") — known
  wrong, not yet corrected. Don't let that wording justify removing
  KTPCvarChecker's polling cadence; match any new docs to CHANGELOG.md's
  accurate phrasing ("when clients respond to cvar queries") instead.
- This repo is never compiled or deployed on its own. Any "bug" surfaced here
  is really a contract question for the consumer that implements or reads the
  callback (KTP-ReHLDS implements it; KTPAMXX/KTPReAPI consume it).

## Workflow
1. No compile step — consumers auto-detect this SDK as a sibling directory
   (e.g. KTPAMXX's `build_linux.sh` checks `../KTPhlsdk`).
2. Any change to a struct consumers read (`NEW_DLL_FUNCTIONS` especially)
   requires a coordinated rebuild of KTPAMXX and KTP-ReHLDS against the new
   header — then each follows its own build/review/stage/verify workflow.
3. Bump this repo's version in README.md + CHANGELOG.md; if the change is
   ABI-visible, name the forced consumer version bumps in the CHANGELOG entry.
4. No md5/deploy verification applies to this repo directly — that happens on
   the rebuilt consumer binaries once staged.
