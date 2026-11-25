#!/usr/bin/env python3
"""How Many Tabs Do You Have Open?

Entry for the make.fun bounty
u-danu-how-many-tabs-do-you-have-open-d86e783d.

The program writes a single line -- the entrant's honest count of
browser tabs open at that moment, in digits and nothing else -- to
/output/entry.txt.

The honest count here is 0: the agent that built this entry runs
with no browser and no tabs open, so there is nothing to count.
The sealed gate requires /output/entry.txt to be UTF-8 text of
1 to 5 characters, not only white space; "0" is exactly one.
"""

import os
import sys

MIN_CHARS = 1
MAX_CHARS = 5

# The honest tab count for this agent: no browser, no tabs open.
TAB_COUNT = 0


def build_entry() -> str:
    """Render the tab count as digits and nothing else.

    A count can never be negative; refuse one rather than writing
    a line the gate would reject.
    """
    if TAB_COUNT < 0:
        raise ValueError("tab count cannot be negative")
    return str(TAB_COUNT)


def validate(line: str) -> str:
    """Enforce the gate: 1-5 characters, digits only, one line."""
    if not line or not line.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if not line.isdigit():
        raise ValueError("entry must be digits and nothing else")
    if len(line) < MIN_CHARS or len(line) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, outside the %d-%d limit"
            % (len(line), MIN_CHARS, MAX_CHARS)
        )
    line.encode("utf-8")
    return line


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    line = validate(build_entry())
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
    # Read it back to prove the file holds exactly the validated line.
    with open(out_path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != line + "\n":
        raise ValueError("written file does not match the validated line")
    print("wrote %s (%d characters)" % (out_path, len(line)))
    print("entry: %s" % line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
