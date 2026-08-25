#!/usr/bin/env python3
"""Assert NEW_DLL_FUNCTIONS in engine/eiface.h only ever grows at the end.

The consumer build cannot catch this: a reordered or removed member still
compiles on both sides and shifts every later function pointer, so the engine
calls through the wrong slot at runtime. The contract is append-only -- no
removal, no reorder, no insertion anywhere but the tail.

Usage:
    check_abi_append_only.py BASE_HEADER HEAD_HEADER   # exit 0 = contract holds
    check_abi_append_only.py --selftest                # prove the gate can fail

A gate that cannot fail is worse than no gate, so --selftest runs fixtures for
append (pass), removal (fail), reorder (fail) and mid-insertion (fail); CI runs
it before the real comparison.
"""
import re
import sys

STRUCT_END = re.compile(r"^\}\s*NEW_DLL_FUNCTIONS\s*;", re.M)
MEMBER = re.compile(r"\(\s*\*\s*(pfn\w+)\s*\)")


def members(text, label):
    """The ordered member names of the NEW_DLL_FUNCTIONS struct in `text`."""
    end = STRUCT_END.search(text)
    if not end:
        sys.exit("ERROR: no NEW_DLL_FUNCTIONS struct found in %s -- refusing to "
                 "pass on a parse failure" % label)
    # The struct is anonymous (typedef struct { ... } NEW_DLL_FUNCTIONS;), so
    # walk back from the terminator to the nearest `typedef struct`.
    start = text.rfind("typedef struct", 0, end.start())
    if start < 0:
        sys.exit("ERROR: no `typedef struct` opener before the NEW_DLL_FUNCTIONS "
                 "terminator in %s" % label)
    body = text[start:end.start()]
    found = MEMBER.findall(body)
    if not found:
        sys.exit("ERROR: NEW_DLL_FUNCTIONS parsed to zero members in %s -- the "
                 "extractor is broken, not the header" % label)
    return found


def check(base_text, head_text):
    """Return a list of violation strings (empty = contract holds)."""
    base = members(base_text, "base")
    head = members(head_text, "head")
    if head[: len(base)] == base:
        return []
    violations = []
    for name in base:
        if name not in head:
            violations.append("REMOVED: %s" % name)
    common = [n for n in head if n in base]
    if common != [n for n in base if n in head]:
        violations.append("REORDERED: base order %s, head order %s"
                          % ([n for n in base if n in head], common))
    for i, name in enumerate(head):
        if name not in base and i < len(base):
            violations.append("INSERTED MID-STRUCT: %s at slot %d (tail begins "
                              "at slot %d)" % (name, i, len(base)))
    return violations or ["PREFIX MISMATCH: base %s vs head %s" % (base, head)]


FIXTURE = """typedef struct
{
    void (*pfnAlpha)(void);
    int  (*pfnBravo)( edict_t *e );
    void (*pfnCharlie)( const edict_t *e, const char *v );
} NEW_DLL_FUNCTIONS;
"""


def selftest():
    cases = [
        ("unchanged", FIXTURE, True),
        ("append at tail",
         FIXTURE.replace("} NEW_DLL_FUNCTIONS;",
                         "    void (*pfnDelta)(void);\n} NEW_DLL_FUNCTIONS;"), True),
        ("removal", FIXTURE.replace("    int  (*pfnBravo)( edict_t *e );\n", ""), False),
        ("reorder", FIXTURE.replace(
            "    int  (*pfnBravo)( edict_t *e );\n    void (*pfnCharlie)( const edict_t *e, const char *v );",
            "    void (*pfnCharlie)( const edict_t *e, const char *v );\n    int  (*pfnBravo)( edict_t *e );"), False),
        ("mid-insertion", FIXTURE.replace(
            "    int  (*pfnBravo)( edict_t *e );",
            "    int  (*pfnBravo)( edict_t *e );\n    void (*pfnDelta)(void);"), False),
    ]
    failed = 0
    for name, head, want_pass in cases:
        got_pass = not check(FIXTURE, head)
        ok = got_pass == want_pass
        failed += 0 if ok else 1
        print("  %-4s %-14s expected %s, got %s"
              % ("ok" if ok else "FAIL", name,
                 "pass" if want_pass else "fail", "pass" if got_pass else "fail"))
    if failed:
        sys.exit("selftest: %d case(s) wrong -- the gate cannot be trusted" % failed)
    print("selftest: all %d cases behave; the gate can fail" % len(cases))


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        selftest()
        return
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8", errors="replace") as f:
        base_text = f.read()
    with open(sys.argv[2], encoding="utf-8", errors="replace") as f:
        head_text = f.read()
    violations = check(base_text, head_text)
    if violations:
        for v in violations:
            print("::error file=engine/eiface.h::NEW_DLL_FUNCTIONS %s" % v)
        sys.exit(1)
    base_n = len(members(base_text, "base"))
    head_n = len(members(head_text, "head"))
    print("NEW_DLL_FUNCTIONS append-only contract holds (%d -> %d members)"
          % (base_n, head_n))


if __name__ == "__main__":
    main()
