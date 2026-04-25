#!/usr/bin/env python3
"""
verify_hierarchy.py — Beads-ID Parent-Child Hierarchy Validator

Confirms that every 2-hyphen Child ID (section) has a matching
1-hyphen Parent ID (base document). Exits with code 1 if orphans
are found (CI-friendly).

Usage:
    python3 verify_hierarchy.py <docs_directory>
"""

import sys
import os

# Allow importing extract_ids from the same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_ids import extract_beads_ids


def verify(directory):
    results = extract_beads_ids(directory)
    ids = set(item['id'] for item in results)

    parents = set(bid for bid in ids if bid.count("-") == 1)
    children = set(bid for bid in ids if bid.count("-") == 2)
    violations = set(bid for bid in ids if bid.count("-") > 2)

    orphans = []
    for child in sorted(children):
        parent_candidate = child.rsplit('-', 1)[0]
        if parent_candidate not in parents:
            orphans.append((child, parent_candidate))

    # --- Report ---
    print("## Beads-ID Hierarchy Verification\n")
    print(f"  Parents  (1 hyphen):  {len(parents)}")
    print(f"  Children (2 hyphens): {len(children)}")
    print(f"  Matched to parent:    {len(children) - len(orphans)}")
    print(f"  Orphans:              {len(orphans)}")

    if violations:
        print(f"\n⚠️  {len(violations)} IDs exceed the 2-hyphen max:")
        for v in sorted(violations):
            print(f"    - {v}")

    if orphans:
        print(f"\n❌ {len(orphans)} orphaned children (missing parent):")
        for child, missing in orphans:
            print(f"    {child}  ->  expected parent: {missing}")
        return 1
    else:
        print("\n✅ All children have valid parents. Zero orphans.")
        return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 verify_hierarchy.py <docs_directory>")
        sys.exit(1)

    target = sys.argv[1]
    if not os.path.exists(target):
        print(f"Error: Path {target} does not exist.")
        sys.exit(1)

    exit_code = verify(target if os.path.isdir(target) else os.path.dirname(target))
    sys.exit(exit_code)
