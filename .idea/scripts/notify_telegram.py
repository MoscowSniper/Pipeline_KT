#!/usr/bin/env python3
import os
import requests
from datetime import datetime
import subprocess

def get_git_info():
    """Получает информацию о Git"""
    try:
        # Получаем последний коммит
        commit_hash = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'],
            text=True
        ).strip()

        # Получаем автора последнего коммита
        author = subprocess.check_output(
            ['git', 'log', '-1', '--pretty=format:%an'],
            text=True
        ).strip()

        return commit_hash, author
    except Exception as e:
        print(f"Ошибка получения Git информации: {e}")
        return "unknown", "unknown"

def send_telegram_message(bot_token, chat_id, message):
    """Отправляет сообщение в Telegram"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

def send_telegram_document(bot_token, chat_id, document_path, caption=""):
    """Отправляет файл в Telegram"""
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    with open(document_path, 'rb') as file:
        files = {'document': file}
        data = {'chat_id': chat_id, 'caption': caption}
        response = requests.post(url, files=files, data=data)
    response.raise_for_status()
    return response.json()

def main():
    # Получаем переменные окружения
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    new_version = os.getenv('NEW_VERSION', 'unknown')
    repository = os.getenv('GITHUB_REPOSITORY', 'unknown/repo')
    docker_username = os.getenv('DOCKER_USERNAME', 'unknown')

    if not bot_token or not chat_id:
        print("❌ TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        return

    # Получаем Git информацию
    commit_hash, author = get_git_info()

    # Текущая дата и время
    current_time = datetime.now().strftime("%Y.%m.%d  %H:%M:%S")

    # Формируем информативное сообщение
    message = f"""
<b>🚀 GITHUB_DEVOPS_BOT</b>
<b>Новый выпуск изменений</b>

<b>Проект:</b> {repository}
<b>Версия:</b> {new_version}
<b>Дата:</b> {current_time}
<b>Автор:</b> {author}

<b>Информация о Git-репозитории</b>
<b>Commit:</b> {commit_hash}
<b>Version:</b> {new_version}

<b>Информация о Docker-репозитории</b>
<b>Владелец:</b> {docker_username}
<b>Название:</b> pipeline-app
<b>Тег:</b> {new_version}
<b>Полное имя:</b> {docker_username}/pipeline-app:{new_version}

#deployment #ci-cd #devops
"""

    try:
        # Отправляем основное сообщение
        send_telegram_message(bot_token, chat_id, message.strip())
        print("✅ Основное сообщение отправлено в Telegram")

        # Отправляем changelog файл
        changelog_path = ".idea/changelog.md"
        if os.path.exists(changelog_path):
            # Получаем размер файла
            file_size = os.path.getsize(changelog_path)
            file_size_kb = round(file_size / 1024, 1)

            send_telegram_document(
                bot_token,
                chat_id,
                changelog_path,
                f"📋 .idea/changelog.md\n{file_size_kb} KB"
            )
            print("✅ Changelog файл отправлен в Telegram")
        else:
            print("⚠️ changelog.md не найден")

    except Exception as e:
        print(f"❌ Ошибка при отправке в Telegram: {e}")
        raise

if __name__ == "__main__":
    main()