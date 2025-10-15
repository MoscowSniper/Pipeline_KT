#!/usr/bin/env python3
# scripts/generate_changelog.py
import subprocess
from pathlib import Path
import sys

def run(cmd):
    return subprocess.check_output(cmd, shell=True, text=True).strip()

def get_latest_tag():
    try:
        return run("git describe --tags --abbrev=0")
    except subprocess.CalledProcessError:
        return None

def get_commits_since(tag):
    if tag:
        cmd = f"git log {tag}..HEAD --pretty=format:'%h - %s (%an)'"
    else:
        cmd = "git log --pretty=format:'%h - %s (%an)'"
    out = run(cmd)
    return out

def prepend_changelog(new_version, branch):
    p = Path(".idea/changelog.md")
    header = f"## {new_version} — branch: {branch}\n\n"
    commits = get_commits_since(get_latest_tag())
    body = commits + "\n\n"
    old = p.read_text() if p.exists() else ""
    p.write_text(header + body + old)
    print("Changelog updated")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: generate_changelog.py <new_version> <branch>")
        sys.exit(2)
    new_version = sys.argv[1]
    branch = sys.argv[2]
    prepend_changelog(new_version, branch)
