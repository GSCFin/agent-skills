#!/usr/bin/env python3
"""ASCII Diagram Alignment Checker & Fixer.

Validates and optionally fixes:
  1. Outer box width consistency (all lines same length)
  2. Inner sub-box column alignment (│ ┌ ┐ └ ┘ at consistent positions)
  3. Floating vertical alignment (Arrows or │ connecting boxes)

Usage:
  python3 check_alignment.py <file> [--lines START:END] [--fix]
  echo "..." | python3 check_alignment.py - [--fix]

Examples:
  python3 check_alignment.py docs/spike.md --lines 52:115
  python3 check_alignment.py docs/spike.md --fix
"""

import sys
import argparse
import os

RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
CYAN = '\033[0;36m'
NC = '\033[0m'

BORDER_CHARS = set('│┌┐└┘├┤┬┴┼▼▲◄►')
LEFT_BORDER = set('│├┌└')
RIGHT_BORDER = set('│┤┐┘')


def parse_args():
    parser = argparse.ArgumentParser(description='ASCII Diagram Alignment Checker & Fixer')
    parser.add_argument('file', help='File to check, or - for stdin')
    parser.add_argument('--lines', help='Line range START:END (1-indexed)', default=None)
    parser.add_argument('--fix', action='store_true', help='Auto-fix alignment issues')
    parser.add_argument('start', nargs='?', type=int, default=None)
    parser.add_argument('end', nargs='?', type=int, default=None)
    return parser.parse_args()


def read_input(args):
    if args.file == '-':
        all_lines = sys.stdin.read().split('\n')
        return all_lines, 1, len(all_lines)

    with open(args.file, 'r') as f:
        all_lines = f.read().split('\n')

    if args.lines:
        parts = args.lines.split(':')
        start = int(parts[0])
        end = int(parts[1]) if len(parts) > 1 else len(all_lines)
    elif args.start is not None:
        start = args.start
        end = args.end if args.end is not None else len(all_lines)
    else:
        start = 1
        end = len(all_lines)

    return all_lines, start, end


def find_boxes(lines, start_line, end_line):
    boxes = []
    in_box = False
    current_box = None

    for i in range(start_line - 1, min(end_line, len(lines))):
        line = lines[i]
        actual_line = i + 1
        stripped = line.lstrip()

        if stripped.startswith(('┌', '╔')) and not in_box:
            in_box = True
            current_box = {
                'start': actual_line,
                'width': len(line),
                'lines': [(actual_line, line)],
            }
        elif stripped.startswith(('└', '╚')) and in_box:
            current_box['lines'].append((actual_line, line))
            current_box['end'] = actual_line
            boxes.append(current_box)
            in_box = False
            current_box = None
        elif in_box:
            current_box['lines'].append((actual_line, line))

    return boxes


def check_outer_width(box):
    # Find expected width based on the left and right border of the first line
    first_ln_txt = box['lines'][0][1]
    left_margin = len(first_ln_txt) - len(first_ln_txt.lstrip())
    # find rightmost border
    right_idx = max((i for i, ch in enumerate(first_ln_txt) if ch in RIGHT_BORDER), default=-1)
    if right_idx == -1:
        expected = len(first_ln_txt)
    else:
        expected = right_idx + 1

    errors = []
    for ln, txt in box['lines']:
        r_idx = max((i for i, ch in enumerate(txt) if ch in RIGHT_BORDER), default=-1)
        w = r_idx + 1 if r_idx != -1 else len(txt.rstrip())
        if w != expected:
            errors.append((ln, w, expected, txt))
    return errors


def find_inner_box_groups(box):
    content = box['lines'][1:-1]
    if not content:
        return []

    groups = []
    current_group = []
    in_inner = False

    for ln, txt in content:
        inner = txt[1:] if txt and txt[0] in LEFT_BORDER else txt

        has_top = '┌' in inner
        has_bottom = '└' in inner
        has_vert = any(c in inner for c in '│▼▲◄►v^')

        if has_top:
            in_inner = True
            current_group = [(ln, txt)]
        elif has_bottom and in_inner:
            current_group.append((ln, txt))
            groups.append(current_group)
            current_group = []
            in_inner = False
        elif in_inner and has_vert:
            current_group.append((ln, txt))

    return groups


def get_border_positions(line, inner_only=True):
    if not line:
        return []

    positions = []
    for i, ch in enumerate(line):
        if ch in BORDER_CHARS:
            positions.append((i, ch))

    if inner_only and len(positions) >= 2:
        if positions[0][1] in LEFT_BORDER and positions[-1][1] in RIGHT_BORDER:
            positions = positions[1:-1]

    return positions


def check_inner_alignment(box):
    groups = find_inner_box_groups(box)
    errors = []

    for group in groups:
        if len(group) < 2:
            continue

        ref_ln, ref_txt = group[0]
        ref_pos = get_border_positions(ref_txt)
        ref_cols = [p for p, _ in ref_pos]

        for ln, txt in group[1:]:
            cur_pos = get_border_positions(txt)
            cur_cols = [p for p, _ in cur_pos]

            if len(cur_cols) == len(ref_cols):
                for j, (rc, cc) in enumerate(zip(ref_cols, cur_cols)):
                    if rc != cc:
                        errors.append((ln, cc, rc, ref_ln, txt))
                        break
            elif len(cur_cols) > 0 and len(ref_cols) > 0:
                if cur_cols[0] != ref_cols[0] or cur_cols[-1] != ref_cols[-1]:
                    errors.append((ln, cur_cols[-1], ref_cols[-1], ref_ln, txt))

    return errors


def get_closest_anchor(lines, ln_idx, col):
    """Search up & down for structural diagram characters to anchor a floating vertical char."""
    search_chars = set('┬┴┼┌┐└┘')
    
    # Search UP
    for r in range(ln_idx - 1, max(-1, ln_idx - 15), -1):
        line = lines[r]
        for c in range(max(0, col - 3), min(len(line), col + 4)):
            if line[c] in search_chars:
                return r, c
                
    # Search DOWN
    for r in range(ln_idx + 1, min(len(lines), ln_idx + 15)):
        line = lines[r]
        for c in range(max(0, col - 3), min(len(line), col + 4)):
            if line[c] in search_chars:
                return r, c
                
    # Fallback: align with another vertical char if strictly above/below
    for r in [ln_idx - 1, ln_idx + 1]:
        if 0 <= r < len(lines):
            line = lines[r]
            for c in range(max(0, col - 3), min(len(line), col + 4)):
                if line[c] in set('│▼▲'):
                    return r, c
                    
    return None, None


def check_floating_verticals(lines, boxes, start_line, end_line):
    """Check floating vertical lines outside boxes."""
    errors = []
    in_box_indices = set()
    for b in boxes:
        for ln_num, _ in b['lines']:
            in_box_indices.add(ln_num - 1)
            
    floating_chars = set('│▼▲')
            
    for i in range(start_line - 1, min(end_line, len(lines))):
        if i in in_box_indices: continue
        line = lines[i]
        
        for c, ch in enumerate(line):
            if ch in floating_chars:
                anchor_r, anchor_c = get_closest_anchor(lines, i, c)
                if anchor_c is not None and anchor_c != c:
                    errors.append((i+1, c, anchor_c, anchor_r+1, line))
    return errors


def fix_outer_width(lines, box, target_width=None):
    if target_width is None:
        target_width = box['width']

    fixes = 0
    for ln, txt in box['lines']:
        idx = ln - 1
        cur = len(txt)
        if cur == target_width:
            continue

        stripped = txt.lstrip()
        leading_spaces = len(txt) - len(stripped)
        
        if not stripped or stripped[0] not in LEFT_BORDER:
            continue

        last_char = stripped.rstrip()[-1] if stripped.rstrip() else ''
        if last_char not in RIGHT_BORDER:
            continue

        inner = stripped[1:-1]
        off = target_width - cur
        if off > 0:
            new_line = (' ' * leading_spaces) + stripped[0] + inner + ' ' * off + last_char
        else:
            inner_stripped = inner.rstrip()
            spaces = len(inner) - len(inner_stripped)
            new_spaces = max(0, spaces + off)
            new_line = (' ' * leading_spaces) + stripped[0] + inner_stripped + ' ' * new_spaces + last_char

        lines[idx] = new_line
        fixes += 1
        print(f"  {CYAN}FIXED{NC} L{ln}: width {cur} → {len(new_line)}")

    return fixes


def fix_inner_alignment(lines, box):
    groups = find_inner_box_groups(box)
    target_width = box['width']
    fixes = 0

    for group in groups:
        if len(group) < 2:
            continue

        ref_ln, ref_txt = group[0]
        ref_pos = get_border_positions(ref_txt)
        ref_cols = [p for p, _ in ref_pos]

        if not ref_cols:
            continue

        for ln, txt in group[1:]:
            idx = ln - 1
            cur_pos = get_border_positions(txt)
            cur_cols = [p for p, _ in cur_pos]

            if len(cur_cols) != len(ref_cols):
                continue

            needs_fix = False
            for rc, cc in zip(ref_cols, cur_cols):
                if rc != cc:
                    needs_fix = True
                    break

            if not needs_fix:
                continue

            new_line = list(txt)
            all_cur = [(i, ch) for i, ch in enumerate(txt) if ch in BORDER_CHARS]
            all_ref_line = [(i, ch) for i, ch in enumerate(ref_txt) if ch in BORDER_CHARS]

            if len(all_cur) != len(all_ref_line):
                continue

            segments = []
            prev_end = 0
            for (cur_p, cur_ch), (ref_p, ref_ch) in zip(all_cur, all_ref_line):
                content = txt[prev_end:cur_p]
                segments.append((ref_p, cur_ch, content))
                prev_end = cur_p + 1

            trailing = txt[prev_end:]

            result = []
            pos = 0
            for ref_p, ch, content in segments:
                needed = ref_p - pos
                if needed > len(content):
                    content = content + ' ' * (needed - len(content))
                elif needed < len(content):
                    trimmed = content.rstrip()
                    content = trimmed + ' ' * max(0, needed - len(trimmed))
                result.append(content)
                result.append(ch)
                pos = ref_p + 1

            rebuilt = ''.join(result) + trailing
            if len(rebuilt) < target_width:
                last_border_idx = max(i for i, c in enumerate(rebuilt) if c in RIGHT_BORDER)
                before = rebuilt[:last_border_idx]
                after = rebuilt[last_border_idx:]
                pad = target_width - len(rebuilt)
                rebuilt = before + ' ' * pad + after
            elif len(rebuilt) > target_width:
                last_border_idx = max(i for i, c in enumerate(rebuilt) if c in RIGHT_BORDER)
                before = rebuilt[:last_border_idx].rstrip()
                after = rebuilt[last_border_idx:]
                needed_spaces = target_width - len(before) - len(after)
                rebuilt = before + ' ' * max(0, needed_spaces) + after

            lines[idx] = rebuilt
            fixes += 1
            print(f"  {CYAN}FIXED{NC} L{ln}: inner borders realigned to match L{ref_ln}")

    return fixes


def fix_floating_verticals(lines, boxes, start_line, end_line):
    in_box_indices = set()
    for b in boxes:
        for ln_num, _ in b['lines']:
            in_box_indices.add(ln_num - 1)
            
    floating_chars = set('│▼▲')
    fixes = 0
            
    for i in range(start_line - 1, min(end_line, len(lines))):
        if i in in_box_indices: continue
        line = lines[i]
        
        chars_to_move = []
        for c, ch in enumerate(line):
            if ch in floating_chars:
                anchor_r, anchor_c = get_closest_anchor(lines, i, c)
                if anchor_c is not None and anchor_c != c:
                    chars_to_move.append((c, ch, anchor_c))
                    
        if not chars_to_move: continue
        
        all_cur = [(p, line[p]) for p in range(len(line)) if line[p] in floating_chars]
        targets = []
        for p, ch in all_cur:
            anchor_r, anchor_c = get_closest_anchor(lines, i, p)
            if anchor_c is not None:
                targets.append((anchor_c, ch))
            else:
                targets.append((p, ch))
                
        segments = []
        prev_end = 0
        for (cur_p, cur_ch), (tgt_p, tgt_ch) in zip(all_cur, targets):
            content = line[prev_end:cur_p]
            segments.append((tgt_p, tgt_ch, content))
            prev_end = cur_p + 1
            
        trailing = line[prev_end:]
        result = []
        pos = 0
        for tgt_p, ch, content in segments:
            needed = tgt_p - pos
            if needed > len(content):
                content = content + ' ' * (needed - len(content))
            elif needed < len(content):
                content = content.rstrip() + ' ' * max(0, needed - len(content.rstrip()))
            result.append(content)
            result.append(ch)
            pos = tgt_p + 1
            
        rebuilt = ''.join(result) + trailing
        lines[i] = rebuilt
        fixes += 1
        print(f"  {CYAN}FIXED{NC} L{i+1}: floating verticals realigned")
        
    return fixes


def main():
    args = parse_args()
    all_lines, start_line, end_line = read_input(args)

    boxes = find_boxes(all_lines, start_line, end_line)

    if not boxes and not any('│' in l or '▼' in l for l in all_lines):
        print(f"{YELLOW}WARN{NC} No box diagrams or vertical drawing characters found in range")
        sys.exit(0)

    total_errors = 0
    total_fixes = 0

    for box in boxes:
        width_errors = check_outer_width(box)
        for ln, actual_w, expected_w, txt in width_errors:
            diff = actual_w - expected_w
            sign = '+' if diff > 0 else ''
            print(f"{RED}ERROR{NC} Line {ln}: width={actual_w} (expected {expected_w}, {sign}{diff})")
            print(f"       {txt}")
            total_errors += 1

        if not width_errors:
            print(f"{GREEN}OK{NC} Box at lines {box['start']}-{box['end']}: "
                  f"all {len(box['lines'])} lines width={box['width']}")

        inner_errors = check_inner_alignment(box)
        for ln, col, expected_col, ref_ln, txt in inner_errors:
            print(f"{RED}ERROR{NC} Line {ln}: inner border at col {col} misaligned "
                  f"(expected col {expected_col}, ref line {ref_ln})")
            print(f"       {txt}")
            total_errors += 1

        if not inner_errors and find_inner_box_groups(box):
            inner_count = sum(len(g) for g in find_inner_box_groups(box))
            print(f"{GREEN}OK{NC}   Inner boxes ({inner_count} lines): "
                  f"all borders aligned")

    float_errors = check_floating_verticals(all_lines, boxes, start_line, end_line)
    for ln, col, expected_col, ref_ln, txt in float_errors:
        print(f"{RED}ERROR{NC} Line {ln}: floating border at col {col} misaligned "
              f"(expected col {expected_col}, ref line {ref_ln})")
        print(f"       {txt}")
        total_errors += 1
        
    if not float_errors:
        print(f"{GREEN}OK{NC}   Floating verticals: all aligned")

    if args.fix and total_errors > 0:
        print(f"\n{CYAN}Fixing alignment issues...{NC}")
        for box in boxes:
            total_fixes += fix_inner_alignment(all_lines, box)
            # Re-update lines in box
            box['lines'] = [(ln, all_lines[ln - 1]) for ln, _ in box['lines']]
            total_fixes += fix_outer_width(all_lines, box)
            
        total_fixes += fix_floating_verticals(all_lines, boxes, start_line, end_line)

    print()
    print("─────────────────────────────────")
    if total_errors == 0:
        print(f"{GREEN}PASS{NC} All elements have consistent alignment")
    elif args.fix and total_fixes > 0:
        print(f"{CYAN}FIXED{NC}: {total_fixes} fix(es) applied")
    else:
        print(f"{RED}FAIL{NC}: {total_errors} error(s)")
    print("─────────────────────────────────")

    if args.fix and total_fixes > 0 and args.file != '-':
        with open(args.file, 'w') as f:
            f.write('\n'.join(all_lines))
        print(f"\n{GREEN}File saved:{NC} {args.file}")

        print(f"\n{CYAN}Re-checking after fix...{NC}\n")
        with open(args.file, 'r') as f:
            recheck_lines = f.read().split('\n')
        recheck_boxes = find_boxes(recheck_lines, start_line, end_line)
        recheck_errors = 0
        
        for box in recheck_boxes:
            w_err = check_outer_width(box)
            i_err = check_inner_alignment(box)
            recheck_errors += len(w_err) + len(i_err)
            
        f_err = check_floating_verticals(recheck_lines, recheck_boxes, start_line, end_line)
        recheck_errors += len(f_err)

        print("─────────────────────────────────")
        if recheck_errors == 0:
            print(f"{GREEN}PASS{NC} All elements clean after fix")
        else:
            print(f"{RED}FAIL{NC}: {recheck_errors} error(s) remain after final check")
        print("─────────────────────────────────")
        sys.exit(recheck_errors)

    sys.exit(total_errors)


if __name__ == '__main__':
    main()
