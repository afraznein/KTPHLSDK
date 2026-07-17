# KTPhlsdk - Claude Code Context

**REQUIRED: Before modifying any header in this repo, invoke the `cpp-dev` skill** (`.claude/skills/cpp-dev/SKILL.md`). It carries the ABI append-only contract, the pfnClientCvarChanged trigger-scope fact, and the coordinated-bump workflow with consumers; do not edit source without it loaded.

## Purpose
Modified Half-Life 1 SDK headers with `pfnClientCvarChanged` callback. This is a **header-only dependency** — no compilation needed. Used at build time by KTPAMXX and KTP-ReHLDS.

## KTP Modification
Single addition to `engine/eiface.h`: `pfnClientCvarChanged` callback in `NEW_DLL_FUNCTIONS` struct (line 525-530). Enables real-time client cvar change detection without polling.

## Project Structure
- `engine/eiface.h` - **The only modified file** (pfnClientCvarChanged added)
- `engine/` - Engine interface headers (used by KTP projects)
- `common/` - Shared definitions
- `public/` - Public interfaces
- `dlls/`, `cl_dll/`, `game_shared/` - Sample code (NOT used by KTP)

## How It's Used
```bash
# KTPAMXX build_linux.sh auto-detects this SDK:
if [ -d "$(pwd)/../KTPhlsdk" ]; then
    export HLSDK="$(pwd)/../KTPhlsdk"
fi
```

Projects that depend on this SDK:
- **KTPAMXX** - Includes `engine/eiface.h` for NEW_DLL_FUNCTIONS
- **KTP-ReHLDS** - Implements the pfnClientCvarChanged callback

## No Build/Deploy Required
Header-only SDK. No compilation, no staging, no deployment.

## Related Projects
- `N:\Nein_\KTP Git Projects\KTPAMXX` - AMX Mod X fork (consumer)
- `N:\Nein_\KTP Git Projects\KTPReHLDS` - ReHLDS fork (implementor)
