# KTP Half-Life SDK

**Version 1.0.0** | Modified Half-Life 1 SDK headers with `pfnClientCvarChanged` callback

A fork of the [Half-Life 1 SDK](https://github.com/ValveSoftware/halflife) that adds a single callback to `NEW_DLL_FUNCTIONS`, enabling real-time client cvar change detection. Used as a build-time dependency by [KTPAMXX](https://github.com/afraznein/KTPAMXX) and [KTP-ReHLDS](https://github.com/afraznein/KTPReHLDS).

Part of the [KTP Competitive Infrastructure](https://github.com/afraznein).

---

## Modification

One callback added to `engine/eiface.h` in the `NEW_DLL_FUNCTIONS` struct:

```cpp
// KTP Custom: Real-time client cvar change notification
// Called whenever a client cvar query response is received from the client
void (*pfnClientCvarChanged)(const edict_t *pEnt, const char *cvarName, const char *value);
```

This enables KTP-ReHLDS to notify KTPAMXX (running as a ReHLDS extension) when clients respond to cvar queries. KTPAMXX fires the `client_cvar_changed` forward to plugins like KTPCvarChecker for real-time anti-cheat enforcement.

**Key difference from existing `pfnCvarValue2`:** `pfnCvarValue2` is a response to explicit `query_client_cvar` calls. `pfnClientCvarChanged` fires for ANY cvar change detected by the engine, providing continuous monitoring.

---

## How It Works

```
Game Client responds to cvar query
         │ Network packet
         ↓
KTP-ReHLDS (engine)
  - Calls pfnClientCvarChanged()
         │ Callback
         ↓
KTPAMXX (extension mode)
  - Fires client_cvar_changed forward
         │ AMX forward
         ↓
KTPCvarChecker (plugin)
  - Validates and enforces cvar values
```

---

## Usage

This is a **header-only SDK** — no compilation needed. Include it as a build dependency:

```bash
# Clone alongside KTP projects
git clone https://github.com/afraznein/KTPHLSDK.git KTPhlsdk

# KTPAMXX and KTP-ReHLDS auto-detect it in the sibling directory
```

---

## Related Projects

**KTP Stack:**
- [KTP-ReHLDS](https://github.com/afraznein/KTPReHLDS) - Implements `pfnClientCvarChanged` in the engine
- [KTPAMXX](https://github.com/afraznein/KTPAMXX) - Receives callbacks, fires `client_cvar_changed` forward
- [KTPCvarChecker](https://github.com/afraznein/KTPCvarChecker) - Real-time cvar enforcement plugin

**Upstream:**
- [Half-Life 1 SDK](https://github.com/ValveSoftware/halflife) - Original Valve SDK

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## License

Half Life 1 SDK License (Valve proprietary, free for non-commercial use). See [LICENSE](LICENSE) for full text.
