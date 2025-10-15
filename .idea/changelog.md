#!/usr/bin/env python3
import subprocess
from pathlib import Path
import sys
from datetime import datetime

def run(cmd):
return subprocess.check_output(cmd, shell=True, text=True).strip()

def get_latest_tag():
try:
return run("git describe --tags --abbrev=0")
except subprocess.CalledProcessError:
return None

def get_commits_since(tag):
if tag:
cmd = f"git log {tag}..HEAD --oneline --pretty=format:'- %s (%an)'"
else:
cmd = "git log --oneline --pretty=format:'- %s (%an)'"
try:
return run(cmd)
except subprocess.CalledProcessError:
return "No commits found"

def prepend_changelog(new_version, branch):
p = Path("changelog.md")

    # Header with version, branch and date
    header = f"""## Version {new_version}

**Branch**: {branch}  
**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Changes**:

"""

    # Get commits since last tag
    latest_tag = get_latest_tag()
    commits = get_commits_since(latest_tag)
    
    # Prepare content
    if latest_tag:
        changes_section = f"Changes since {latest_tag}:\n\n{commits}\n\n"
    else:
        changes_section = f"Initial release:\n\n{commits}\n\n"
    
    # Read existing content and prepend new release
    old_content = p.read_text() if p.exists() else "# Changelog\n\n"
    
    # Insert after the header
    if old_content.startswith("# Changelog"):
        parts = old_content.split("\n", 2)
        if len(parts) >= 3:
            new_content = parts[0] + "\n" + parts[1] + "\n\n" + header + changes_section + parts[2]
        else:
            new_content = old_content + "\n\n" + header + changes_section
    else:
        new_content = "# Changelog\n\n" + header + changes_section + old_content
    
    p.write_text(new_content)
    print(f"Changelog updated for version {new_version}")

if __name__ == "__main__":
if len(sys.argv) < 3:
print("Usage: generate_changelog.py <new_version> <branch>")
sys.exit(1)

    new_version = sys.argv[1]
    branch = sys.argv[2]
    prepend_changelog(new_version, branch)