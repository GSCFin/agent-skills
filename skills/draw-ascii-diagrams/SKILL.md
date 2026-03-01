---
name: ascii
description: Generates ASCII diagrams for flows, architectures, and processes. Use when asked to create an ASCII diagram or visualize something in text.
argument-hint: description of the diagram to generate
---

# ASCII Diagram Generator

Create ASCII diagrams for flows, architectures, and processes.

## Instructions

Generate an ASCII diagram based on the user's description provided in `$ARGUMENTS`.

### Phase 1: Analyze the Request

1. Parse the `$ARGUMENTS` to understand what flow/diagram is needed
2. Identify the type of diagram:
   - **Flow diagram**: Sequential steps with arrows
   - **Architecture diagram**: Boxes representing components
   - **Sequence diagram**: Interactions between entities
   - **Tree/hierarchy**: Parent-child relationships
   - **State machine**: States and transitions

### Phase 2: Create the Diagram

Generate a clean ASCII diagram using these conventions:

**Boxes**:

```
┌─────────────┐
│   Label     │
└─────────────┘
```

**Arrows**:

- Horizontal: `───>` or `<───`
- Vertical: `│` with `▼` or `▲`
- Bidirectional: `<──>`

**Flow connections**:

```
┌───────┐     ┌───────┐
│ Step1 │────>│ Step2 │
└───────┘     └───────┘
```

**Decision points**:

```
    ┌───────┐
    │ Check │
    └───┬───┘
        │
   ┌────┴────┐
   ▼         ▼
┌─────┐   ┌─────┐
│ Yes │   │ No  │
└─────┘   └─────┘
```

**Guidelines**:

- Keep boxes aligned and evenly spaced
- Use consistent widths where possible
- Add labels to arrows when needed: `──(label)──>`
- Use comments/notes outside the diagram for context
- Keep it readable — don't overcrowd

### Phase 2.5: Quality Check — Box Alignment Validation

**CRITICAL**: After creating any diagram with boxes (`┌─┐`, `├─┤`, `└─┘`), you MUST validate alignment before presenting.

**The Problem**: In monospace fonts, every character is the same width. If one line has 72 characters between `│...│` and another has 73, the right border `│` will be visually misaligned. This looks broken.

**Validation Rules**:

1. **Every line between `┌` (top) and `└` (bottom) of a box MUST have the exact same character count** (including the border characters themselves)
2. The `┌───┐` top border, all `│...│` content lines, any `├───┤` dividers, and the `└───┘` bottom border must ALL be the same width
3. **Count characters, not visual width** — a line that "looks right" may have trailing spaces or missing padding

**How to check**:

Method 1 — Use the validation script:

```bash
# Check a specific file range
python3 .agents/skills/draw-ascii-diagrams/scripts/check_alignment.py <file> --lines <start>:<end>

# Check and auto-fix alignment issues
python3 .agents/skills/draw-ascii-diagrams/scripts/check_alignment.py <file> --fix

# Check a range and auto-fix
python3 .agents/skills/draw-ascii-diagrams/scripts/check_alignment.py <file> --lines <start>:<end> --fix

# Legacy wrapper (backward compat)
bash .agents/skills/draw-ascii-diagrams/scripts/check_alignment.sh <file> <start> <end>
```

The script will output:

```
OK Box at lines 52-115: all 64 lines width=72
```

or:

```
ERROR Line 54: width=73 (expected 72, +1)
       │                                                                       │
```

Method 2 — Manual verification (when script is unavailable):

```bash
# Extract the diagram lines and check their lengths
sed -n '<start>,<end>p' <file> | awk '{ print length, $0 }' | sort -n | head -5
sed -n '<start>,<end>p' <file> | awk '{ print length, $0 }' | sort -rn | head -5
```

If the shortest and longest lines have different lengths, there's a misalignment.

**Fix strategy**: Pad shorter lines with spaces before the closing `│` to match the widest line's width. Never truncate content — always pad.

- **Vietnamese Characters are SAFE**: Vietnamese characters with diacritics (ệ, ổ, ầ) are treated as exactly 1 character width. You CAN and SHOULD use proper Vietnamese with diacritics inside ASCII diagrams. They do not break alignment.
- **NO special characters or emoji** (🧑📋📐🔧🤖⚠️❌✅ etc.) inside diagrams — use only Vietnamese or English words instead. Emoji have unpredictable display widths and break alignment.
- Tabs vs spaces — NEVER use tabs inside ASCII diagrams
- Trailing whitespace — ensure padding spaces are present, not stripped by editors

### Phase 3: Present the Diagram

Display the completed ASCII diagram in a code block:

```
[Your ASCII diagram here]
```

### Phase 4: Ask About Saving

After showing the diagram, ask the user what they'd like to do:

```
What would you like to do with this diagram?

1. Save to a new markdown file
2. Add to an existing file
3. Don't save (just viewing)
```

Use the AskUserQuestion tool with these options:

- **Save to new file**: Ask for filename, create `[filename].md` with the diagram in a code block
- **Add to existing file**: Ask which file, then append the diagram to that file
- **Don't save**: Acknowledge and end

### Saving Behavior

**New file format**:

```markdown
# [Title based on diagram content]

[ASCII diagram in code block]

---

_Generated with /ascii_
```

**Appending to existing file**:

- Add a newline separator
- Insert the diagram in a code block
- Don't modify existing content

## Examples

**Input**: `/ascii user login flow`

**Output**:

```
┌──────────┐     ┌────────────┐     ┌──────────────┐
│  User    │────>│ Login Form │────>│ Validate     │
└──────────┘     └────────────┘     └──────┬───────┘
                                           │
                                    ┌──────┴──────┐
                                    ▼             ▼
                              ┌─────────┐   ┌─────────┐
                              │ Success │   │ Error   │
                              └────┬────┘   └────┬────┘
                                   │             │
                                   ▼             ▼
                              ┌─────────┐   ┌─────────┐
                              │Dashboard│   │ Retry   │
                              └─────────┘   └─────────┘
```

**Input**: `/ascii api request lifecycle`

**Output**:

```
┌────────┐    ┌────────────┐    ┌────────────┐    ┌──────────┐
│ Client │───>│ Middleware │───>│ Controller │───>│ Service  │
└────────┘    └────────────┘    └────────────┘    └────┬─────┘
     ▲                                                 │
     │                                                 ▼
     │                                           ┌──────────┐
     │                                           │ Database │
     │                                           └────┬─────┘
     │                                                │
     └────────────────────────────────────────────────┘
                        Response
```
