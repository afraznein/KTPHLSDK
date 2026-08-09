# Changelog

All notable changes to KTP Half-Life SDK will be documented in this file.

This project is a fork of the Valve Half-Life 1 SDK with KTP-specific modifications.

## KTP Modifications

### [1.0.1] - 2026-08-09

#### Documentation
- Corrected the `pfnClientCvarChanged` description at all four sites that carried it
  (`README.md`, `engine/eiface.h`, this file, `CLAUDE.md`). All four called it continuous
  cvar-change monitoring that removes polling. It is neither: the callback fires on every
  cvar-query **response** the engine receives, and its real advantage over `pfnCvarValue2`
  is that a consumer sees responses to queries it did not itself issue. Nothing fires for a
  cvar nobody queried, so a client can change one between queries and go unobserved —
  enforcement still depends on a query cadence. The docs removed the plugin's need to poll
  and then claimed the need to *ask* had gone with it, which is the sentence an enforcement
  design would have been built on. The 1.0.0 entry below was edited in place rather than
  left standing, because a wrong technical claim in a changelog is read as fact.

### [1.0.0] - 2025-11-27

#### Added
- `pfnClientCvarChanged` callback to `NEW_DLL_FUNCTIONS` structure in `engine/eiface.h`
- Enables engine implementations (like KTP-ReHLDS) to notify game DLLs when clients respond to cvar queries
- Lets a game DLL observe cvar-query responses it did not itself request (no plugin-side polling); still query-driven, so it is not continuous change detection

#### Documentation
- Added comprehensive README with usage examples (2025-11-28)
- Integration details for KTP-ReHLDS and KTPAMXX
- Proper licensing information for Valve Half-Life 1 SDK

---

## Upstream History

For upstream Half-Life SDK history, see: https://github.com/ValveSoftware/halflife

The base SDK includes patches from:
- Will Day's patchsets (2013)
- Scott Ehlert's AMX Mod X compatibility patches (2013)
- Valve's upstream updates (2013)

---

## Credits

**KTP Modifications:**
- **Nein_** ([@afraznein](https://github.com/afraznein)) - Added pfnClientCvarChanged callback

**Original SDK:**
- **Valve Corporation** - Half-Life 1 SDK
