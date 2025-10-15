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

def get_commit_count(tag):
"""Получить количество коммитов с последнего тега"""
if tag:
try:
return run(f"git rev-list {tag}..HEAD --count")
except:
return "?"
return "?"

def prepend_changelog(new_version, branch):
p = Path("changelog.md")

    # Получаем информацию для заголовка
    latest_tag = get_latest_tag()
    commit_count = get_commit_count(latest_tag)
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Красивый заголовок с иконками
    header = f"""## 🚀 Version {new_version}

**📅 Date**: {current_date}  
**🌿 Branch**: `{branch}`  
**📊 Commits since last release**: {commit_count}  
**🏷️ Previous version**: {latest_tag if latest_tag else 'First release'}

### 📋 Changes

"""

    # Получаем коммиты
    commits = get_commits_since(latest_tag)
    
    # Подготавливаем секцию с коммитами
    if latest_tag:
        changes_section = f"**Changes since {latest_tag}:**\n\n{commits}\n\n"
    else:
        changes_section = f"**Initial release:**\n\n{commits}\n\n"
    
    # Разделитель между версиями
    separator = "---\n\n"
    
    # Читаем существующее содержимое и добавляем новую версию в начало
    old_content = p.read_text() if p.exists() else "# 📄 Changelog\n\n"
    
    # Вставляем после заголовка
    if old_content.startswith("# 📄 Changelog"):
        parts = old_content.split("\n", 2)
        if len(parts) >= 3:
            new_content = parts[0] + "\n" + parts[1] + "\n\n" + header + changes_section + separator + parts[2]
        else:
            new_content = old_content + "\n\n" + header + changes_section + separator
    else:
        new_content = "# 📄 Changelog\n\n" + header + changes_section + separator + old_content
    
    p.write_text(new_content)
    print(f"✅ Changelog updated for version {new_version}")

if __name__ == "__main__":
if len(sys.argv) < 3:
print("Usage: generate_changelog.py <new_version> <branch>")
sys.exit(1)

    new_version = sys.argv[1]
    branch = sys.argv[2]
    prepend_changelog(new_version, branch)