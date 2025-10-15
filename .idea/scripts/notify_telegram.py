#!/usr/bin/env python3
import os
import requests
from pathlib import Path

def send_telegram_message(bot_token, chat_id, message):
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
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    with open(document_path, 'rb') as file:
        files = {'document': file}
        data = {'chat_id': chat_id, 'caption': caption}
        response = requests.post(url, files=files, data=data)
    response.raise_for_status()
    return response.json()

def main():
    # Get environment variables
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    new_version = os.getenv('NEW_VERSION', 'unknown')
    repository = os.getenv('GITHUB_REPOSITORY', 'unknown/repo')

    if not bot_token or not chat_id:
        print("❌ TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        return

    # Prepare message
    message = f"""
🚀 <b>New Release Deployed!</b>

📦 <b>Version:</b> <code>{new_version}</code>
📚 <b>Repository:</b> {repository}
🔗 <b>Docker Image:</b> {os.getenv('DOCKER_USERNAME', 'user')}/pipeline-app:{new_version}

✅ <i>All stages passed successfully</i>

#deployment #ci-cd
"""

    try:
        # Send message
        send_telegram_message(bot_token, chat_id, message.strip())
        print("✅ Message sent to Telegram")

        # Send changelog file
        changelog_path = Path("changelog.md")
        if changelog_path.exists():
            send_telegram_document(
                bot_token,
                chat_id,
                "changelog.md",
                f"📋 Full changelog for version {new_version}"
            )
            print("✅ Changelog file sent to Telegram")
        else:
            print("⚠️ changelog.md not found")

    except Exception as e:
        print(f"❌ Error sending to Telegram: {e}")
        raise

if __name__ == "__main__":
    main()