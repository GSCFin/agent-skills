import os
import re
import json
import sys
import collections

def extract_beads_ids(directory):
    # Regex matching: <!-- beads-id: prd-tplan-s1 -->
    pattern_simple = re.compile(r'<!--\s*beads-id:\s*([a-zA-Z0-9_-]+)\s*-->')
    # Regex matching: <!-- beads-id: pln-rdmap-s3 | satisfies: prd-tplan-s1 -->
    pattern_complex = re.compile(r'<!--\s*beads-id:\s*([a-zA-Z0-9_-]+)\s*\|\s*satisfies:\s*([a-zA-Z0-9_,-]+)\s*-->')
    
    results = []

    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith('.md'):
                continue
                
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line_idx, line in enumerate(lines):
                # Check complex pattern first (with satisfies)
                match_complex = pattern_complex.search(line)
                if match_complex:
                    beads_id = match_complex.group(1).strip()
                    satisfies = [s.strip() for s in match_complex.group(2).split(',')]
                    results.append({
                        "id": beads_id,
                        "file": filepath,
                        "line": line_idx + 1,
                        "satisfies": satisfies,
                        "type": "complex"
                    })
                    continue
                
                # Fallback to simple pattern (just ID)
                match_simple = pattern_simple.search(line)
                if match_simple:
                    beads_id = match_simple.group(1).strip()
                    results.append({
                        "id": beads_id,
                        "file": filepath,
                        "line": line_idx + 1,
                        "satisfies": [],
                        "type": "simple"
                    })
                    
    return results

def print_stats(results):
    """Print a hyphen-count summary table instead of raw JSON."""
    ids = set(item['id'] for item in results)
    hyphen_counts = collections.defaultdict(list)
    
    for bead_id in sorted(ids):
        count = bead_id.count("-")
        hyphen_counts[count].append(bead_id)
    
    print(f"Total Unique Beads: {len(ids)}\n")
    
    for count in sorted(hyphen_counts.keys()):
        beads = hyphen_counts[count]
        label = "Parents (base docs)" if count == 1 else "Children (sections)" if count == 2 else f"Other ({count} hyphens)"
        print(f"  {count} hyphens -> {len(beads):>4} beads  [{label}]")
    
    print()
    
    # Warn about any IDs with >2 hyphens
    violations = [bid for bid in ids if bid.count("-") > 2]
    if violations:
        print(f"⚠️  WARNING: {len(violations)} IDs exceed the 2-hyphen max:")
        for v in sorted(violations):
            print(f"    - {v}")
    else:
        print("✅ All IDs comply with the 2-hyphen max convention.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_ids.py <target_directory_or_file> [--stats]")
        sys.exit(1)
        
    target_path = sys.argv[1]
    show_stats = "--stats" in sys.argv
    
    if not os.path.exists(target_path):
        print(f"Error: Path {target_path} does not exist.")
        sys.exit(1)
        
    if os.path.isfile(target_path):
        target_dir = os.path.dirname(target_path)
    else:
        target_dir = target_path
        
    extracted = extract_beads_ids(target_dir)
    
    if show_stats:
        print_stats(extracted)
    else:
        print(json.dumps(extracted, indent=2))
