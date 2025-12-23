# Changelog

All notable changes to KTP Half-Life SDK will be documented in this file.

This project is a fork of the Valve Half-Life 1 SDK with KTP-specific modifications.

## KTP Modifications

### [1.0.0] - 2025-11-27

#### Added
- `pfnClientCvarChanged` callback to `NEW_DLL_FUNCTIONS` structure in `engine/eiface.h`
- Enables engine implementations (like KTP-ReHLDS) to notify game DLLs when clients respond to cvar queries
- Required for real-time client cvar monitoring without polling

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
