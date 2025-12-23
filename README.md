# KTP Half-Life SDK

**Modified Half-Life 1 SDK headers with pfnClientCvarChanged callback support**

This is a fork of the Half-Life 1 SDK with additions to support real-time client cvar change detection. The primary modification adds the `pfnClientCvarChanged` callback to the engine DLL function table, enabling engine implementations like [KTP-ReHLDS](https://github.com/afraznein/KTPReHLDS) to notify metamod plugins when clients respond to cvar queries.

Part of the [KTP Competitive Infrastructure](https://github.com/afraznein).

---

## 🎯 What is This?

The Half-Life 1 SDK provides header files and interfaces for creating mods and server plugins. This fork adds **one critical callback** that enables real-time client cvar monitoring for anti-cheat systems.

### Why This Fork?

Standard HL1 SDK does not expose client cvar query responses to metamod plugins. This fork adds:

- ✅ `pfnClientCvarChanged` callback definition in `NEW_DLL_FUNCTIONS`
- ✅ Enables engine-level cvar change notifications
- ✅ Required for KTP-ReHLDS and KTPAMXX integration
- ✅ Maintains full compatibility with existing mods

---

## ✨ Modifications

### Added Callback: `pfnClientCvarChanged`

**File Modified:** `engine/eiface.h`

**Change:** Added to `NEW_DLL_FUNCTIONS` structure:

```cpp
typedef struct
{
    // ... existing functions ...

    // KTP Addition: Client cvar change callback
    void (*pfnClientCvarChanged)(const edict_t *pEdict, const char *cvar, const char *value);

} NEW_DLL_FUNCTIONS;
```

**Purpose:**
- Notifies game DLLs when a client responds to a cvar query
- Enables real-time anti-cheat cvar monitoring
- Used by KTP-ReHLDS to forward events to KTPAMXX
- Zero performance impact (callback-driven, not polling)

**Usage Example (in game DLL):**
```cpp
void ClientCvarChanged(const edict_t *pEdict, const char *cvar, const char *value) {
    int client_id = ENTINDEX(pEdict);

    // Forward to metamod plugins (e.g., KTPAMXX)
    if (strcmp(cvar, "r_fullbright") == 0) {
        float val = atof(value);
        if (val != 0.0f) {
            // Violation detected
            ServerPrint("Player %d violated r_fullbright: %f\n", client_id, val);
        }
    }
}
```

---

## 🔗 Related Projects

This SDK fork is part of the KTP stack that enables real-time client monitoring:

**🔧 SDK Layer:**
- **[KTPHLSDK](https://github.com/afraznein/KTPHLSDK)** - This project (Modified SDK headers)

**🎮 Engine Layer:**
- **[KTP-ReHLDS](https://github.com/afraznein/KTPReHLDS)** - Modified Half-Life engine implementing pfnClientCvarChanged

**🔌 Metamod Layer:**
- **[KTPAMXX](https://github.com/afraznein/KTPAMXX)** - Modified AMX Mod X receiving callbacks from KTP-ReHLDS

**🛡️ Plugin Layer:**
- **[KTPCvarChecker](https://github.com/afraznein/KTPCvarChecker)** - Real-time anti-cheat cvar enforcement

---

## 🚀 How It Works

```
┌─────────────────────────────────────┐
│  Game Client                        │
│  - Server queries cvar              │
│  - Client responds with value       │
└────────────────┬────────────────────┘
                 │ Network packet
                 ↓
┌─────────────────────────────────────┐
│  KTP-ReHLDS (Modified Engine)       │
│  - Uses NEW_DLL_FUNCTIONS           │
│  - Calls pfnClientCvarChanged       │
└────────────────┬────────────────────┘
                 │ Callback
                 ↓
┌─────────────────────────────────────┐
│  Game DLL / Metamod                 │
│  - Receives callback                │
│  - Forwards to KTPAMXX              │
└────────────────┬────────────────────┘
                 │ Forward
                 ↓
┌─────────────────────────────────────┐
│  AMX Plugin (KTPCvarChecker)        │
│  - Validates cvar value             │
│  - Enforces correct value           │
└─────────────────────────────────────┘
```

---

## 📦 Usage

### For Mod Developers

This SDK is used when **building mods or engine modifications** that need to detect client cvar changes.

**Include in your project:**
```cpp
#include "eiface.h"

// Implement the callback
void GameDLLInit(void) {
    // ... existing init code ...

    // Register the callback if available
    DLL_FUNCTIONS *pFunctionTable = ...;
    pFunctionTable->pfnClientCvarChanged = ClientCvarChanged;
}

void ClientCvarChanged(const edict_t *pEdict, const char *cvar, const char *value) {
    // Handle cvar change
}
```

### For Engine Developers

When building a Half-Life engine (like ReHLDS), this SDK provides the necessary headers to implement `pfnClientCvarChanged`:

1. Include this SDK in your engine build
2. Implement the callback in your engine code
3. Call the callback when clients respond to cvar queries
4. Game DLLs will receive notifications

---

## 🔧 Building

This is a **header-only SDK** - no compilation needed. Simply include the headers in your mod or engine project.

**For mods:**
```bash
# Clone the SDK
git clone https://github.com/afraznein/KTPHLSDK.git

# Include in your project
# Add hlsdk/engine/ to your include path
```

**For engines (like KTP-ReHLDS):**
```bash
# Clone as submodule or dependency
git submodule add https://github.com/afraznein/KTPHLSDK.git hlsdk

# Reference in your CMakeLists.txt or Makefile
include_directories(hlsdk/engine)
```

---

## 📝 Version History

### KTP Modifications

- **2025-11-27** - Added `pfnClientCvarChanged` callback to `NEW_DLL_FUNCTIONS`
- **2025-11-28** - Added comprehensive documentation
- **Base Version** - Forked from Half-Life 1 SDK by Valve

### Upstream SDK

For upstream Half-Life SDK history, see: https://github.com/ValveSoftware/halflife

---

## 📄 License

**Half Life 1 SDK License** (Valve proprietary, free for non-commercial use)

```
Half Life 1 SDK Copyright© Valve Corp.

You may, free of charge, download and use the SDK to develop a modified
Valve game running on the Half-Life engine. You may distribute your
modified Valve game in source and object code form, but only for free.

Any distribution of this SDK must include this license.txt and
third_party_licenses.txt.
```

See [LICENSE](LICENSE) file for complete license text.

**IMPORTANT:** This SDK may only be used for **non-commercial purposes**. For commercial use, contact Valve at sourceengine@valvesoftware.com.

---

## 🙏 Credits

**KTP Modifications:**
- **Nein_** ([@afraznein](https://github.com/afraznein)) - Added pfnClientCvarChanged callback

**Original SDK:**
- **Valve Corporation** - Half-Life 1 SDK
- **Half-Life Community** - Continued mod development

---

## 🔗 Links

- **GitHub**: https://github.com/afraznein/KTPHLSDK
- **KTP Infrastructure**: https://github.com/afraznein
- **Upstream HL1 SDK**: https://github.com/ValveSoftware/halflife
- **Valve Developer Community**: https://developer.valvesoftware.com/

---

## ⚠️ Important Notes

### Requirements

- ✅ Header-only SDK (no compilation needed)
- ✅ Compatible with existing Half-Life mods
- ✅ `pfnClientCvarChanged` is **optional** - mods not using it work unchanged

### Compatibility

- ✅ **Fully backwards compatible** - Existing mods work without changes
- ✅ **Optional callback** - Only use if you need cvar change detection
- ✅ **Engine-agnostic** - Works with any Half-Life engine (HLDS, ReHLDS, etc.)
- ⚠️ **Callback only works** if engine implements it (like KTP-ReHLDS)

### Usage

**For mod developers:**
- Include this SDK in your project to access the new callback
- Implement `pfnClientCvarChanged` in your game DLL if needed
- Callback will only fire if running on supporting engine

**For engine developers:**
- Reference this SDK for header definitions
- Implement the callback in your engine when clients respond to cvar queries
- See [KTP-ReHLDS](https://github.com/afraznein/KTPReHLDS) for implementation example

---

## 🐛 Reporting Issues

For issues with:
- **pfnClientCvarChanged callback** - Open issue on this repo
- **Standard Half-Life SDK** - See [upstream repository](https://github.com/ValveSoftware/halflife)
- **KTP-ReHLDS integration** - See [KTP-ReHLDS repo](https://github.com/afraznein/KTPReHLDS)

---

**KTP Half-Life SDK** - Enabling real-time client monitoring for Half-Life engines. 🛡️
