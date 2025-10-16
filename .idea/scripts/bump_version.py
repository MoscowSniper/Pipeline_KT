#!/usr/bin/env python3
# scripts/bump_version.py
import sys
from pathlib import Path

def parse_version(s):
    parts = s.strip().split('.')
    return [int(p) for p in parts]

def version_to_str(v):
    return '.'.join(str(x) for x in v)

def bump_version(old_version, bump_type):
    v = parse_version(old_version)
    # Ensure at least 3 components
    while len(v) < 3:
        v.append(0)
    if bump_type == 'feature':
        # increase minor (v[1]) and zero-out patch fix
        v[1] += 1
        v[2] = 0
    elif bump_type == 'hotfix':
        # increase patch .
        v[2] += 1
    else:
        raise ValueError("bump_type must be 'feature' or 'hotfix'")
    return version_to_str(v)

def main():
    if len(sys.argv) < 2:
        print("Usage: bump_version.py <feature|hotfix> [version_file]")
        sys.exit(2)
    bump_type = sys.argv[1]
    vf = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('.idea/version.txt')
    old = vf.read_text().strip()
    new = bump_version(old, bump_type)
    vf.write_text(new + "\n")
    print(f"{old} -> {new}")

if __name__ == "__main__":
    main()
