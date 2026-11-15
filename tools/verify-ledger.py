#!/usr/bin/env python3
"""Infraveil local ledger verifier.

Runs entirely on your machine. It re-hashes your agent's audit ledger and
confirms the hash chain is intact, then (optionally) checks that the final
head matches the anchor Infraveil holds for that agent (shown in your
dashboard). Nothing here trusts Infraveil: it is plain stdlib Python you can
read top to bottom and reimplement in any language.

What this proves, precisely:
  - the retained ledger segment is internally consistent (no edit, deletion,
    insertion, reorder, or sequence gap within it); and
  - (with --head) its final hash equals the anchor value you supplied.
What it does NOT prove on its own: that the anchor itself is authentic. The
anchor comes from an Infraveil-rendered dashboard, so a matching anchor means
"my local chain ends where the dashboard says it does" -- not that the anchor
was never rewritten. External timestamping / a public transparency log would
strengthen that (on our roadmap).

Usage:
    python verify-ledger.py /path/to/agent_audit_<id>.jsonl [--head <anchor>]

Old rotated segments (.1) are read first if present. Segments rotated out
beyond .1 cannot be reconstructed, so verification covers the retained window
(which may start at a sequence > 1).
"""
import sys, os, json, hashlib


def _canonical(obj):
    return json.dumps(obj, separators=(",", ":"), sort_keys=True).encode("utf-8")


def verify(lines):
    prev_hash = None
    prev_seq = None
    start_seq = None
    agent_id = None
    client_id = None
    count = 0
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        count += 1
        rec = json.loads(raw)
        stored = rec.pop("hash", None)
        if stored is None:
            return False, f"entry {count}: no hash field", None
        if hashlib.sha256(_canonical(rec)).hexdigest() != stored:
            return False, f"TAMPERED at seq {rec.get('seq')}: entry was modified (hash mismatch)", None
        seq = rec.get("seq")
        if prev_hash is None:
            start_seq = seq
            agent_id = rec.get("agent_id")
            client_id = rec.get("client_id")
        else:
            if rec.get("prev", "") != prev_hash:
                return False, f"BROKEN CHAIN at seq {seq}: prev link does not match the entry before it (insertion or deletion)", None
            if seq != prev_seq + 1:
                return False, f"SEQUENCE GAP: expected seq {prev_seq + 1}, found {seq}", None
            if rec.get("agent_id") != agent_id or rec.get("client_id") != client_id:
                return False, f"IDENTITY MIX at seq {seq}: entry belongs to a different agent/client", None
        prev_hash = stored
        prev_seq = seq
    if prev_hash is None:
        return False, "no entries", None
    genesis = (start_seq == 1)
    return True, {"head": prev_hash, "start": start_seq, "end": prev_seq, "count": count, "genesis": genesis}, prev_hash


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    head = None
    if "--head" in sys.argv:
        i = sys.argv.index("--head")
        if i + 1 < len(sys.argv):
            head = sys.argv[i + 1].strip()
    if not args:
        print(__doc__)
        return 2
    path = args[0]
    lines = []
    for p in ([path + ".1"] if os.path.exists(path + ".1") else []) + [path]:
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                lines.extend(f.readlines())
    if not lines:
        print("No ledger entries found at", path)
        return 2

    ok, info, final_head = verify(lines)
    if not ok:
        print("LEDGER INVALID:", info)
        return 1

    if info["genesis"]:
        print(f"Ledger intact from genesis: {info['count']} entries (seq 1..{info['end']}), hash chain verified.")
    else:
        print(f"Retained ledger segment intact: {info['count']} entries (seq {info['start']}..{info['end']}), hash chain verified.")
        print("  (Earlier entries were rotated out and cannot be checked here -- this is the retained window.)")
    print("Final head:", final_head)

    if head is not None:
        if head.strip().lower() == final_head.lower():
            print("MATCH: the retained local ledger's final hash matches the supplied anchor.")
            print("  (This confirms your local chain ends at that hash. The anchor is supplied by you")
            print("   from the dashboard and is not independently authenticated by this tool.)")
        else:
            print("MISMATCH: the anchor you supplied does NOT match your ledger's final hash.")
            print("  anchor :", head)
            print("  local  :", final_head)
            return 1
    else:
        print("(Pass --head <value from your dashboard> to also check it against the anchor we hold.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
