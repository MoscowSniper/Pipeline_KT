#!/usr/bin/env python3
import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# 🔍 --- Умный поиск .env ---
def find_env_file():
    """Пытается найти .env в стандартных местах."""
    possible_paths = [
        Path(__file__).resolve().parents[2] / ".env",  # корень проекта
        Path(__file__).resolve().parents[1] / ".env",  # если .env в .idea
        Path(__file__).resolve().parent / ".env",      # рядом со скриптом
    ]
    for path in possible_paths:
        if path.exists():
            print(f"✅ Найден .env: {path}")
            return path
    print("⚠️ .env не найден в стандартных местах.")
    return None

# --- Загружаем .env ---
env_path = find_env_file()
if env_path:
    load_dotenv(dotenv_path=env_path)
else:
    print("❌ Не удалось загрузить .env, проверь расположение файла.")
    sys.exit(2)

# --- Читаем переменные ---
BOT = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT = os.getenv("TELEGRAM_CHAT_ID")

def send_text(msg):
    url = f"https://api.telegram.org/bot{BOT}/sendMessage"
    resp = requests.post(url, json={"chat_id": CHAT, "text": msg, "parse_mode": "HTML"})
    resp.raise_for_status()
    return resp.json()

def send_changelog_file(filepath, caption):
    url = f"https://api.telegram.org/bot{BOT}/sendDocument"
    with open(filepath, "rb") as f:
        files = {"document": f}
        data = {"chat_id": CHAT, "caption": caption}
        resp = requests.post(url, data=data, files=files)
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    if not BOT or not CHAT:
        print("❌ TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID не найдены в окружении!")
        sys.exit(2)

    version = os.getenv("NEW_VERSION", "unknown")
    repo = os.getenv("GITHUB_REPOSITORY", "")
    release_url = os.getenv("RELEASE_URL", "")

    text = f"🚀 Новый релиз: <b>{version}</b>\nРепозиторий: {repo}\n{release_url}"

    try:
        send_text(text)
        print("✅ Сообщение успешно отправлено в Telegram!")
    except Exception as e:
        print(f"❌ Ошибка при отправке сообщения: {e}")
        sys.exit(1)

    if Path(".idea/changelog.md").exists():
        try:
            send_changelog_file("changelog.md", f"📜 Changelog для {version}")
            print("✅ changelog.md успешно отправлен!")
        except Exception as e:
            print(f"⚠️ Не удалось отправить changelog: {e}")
