# check_env.py
import os
from pathlib import Path
from dotenv import load_dotenv



env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)



# Проверим, существует ли файл
if not env_path.exists():
    print("❌ Файл .env не найден!")
else:
    print("✅ Файл .env найден.")

# Загружаем переменные
load_dotenv(dotenv_path=env_path)

# Проверяем значения
bot = os.getenv("TELEGRAM_BOT_TOKEN")
chat = os.getenv("TELEGRAM_CHAT_ID")

print(f"BOT_TOKEN: {bot}")
print(f"CHAT_ID: {chat}")

if bot and chat:
    print("\n✅ Всё отлично! Переменные окружения загружены корректно.")
else:
    print("\n⚠️ Переменные не загрузились. Проверь имена и расположение .env файла.")
