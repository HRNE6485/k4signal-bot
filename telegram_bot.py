import os
import requests
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")

def send_telegram_message(text, to="channel"):
    chat_id = CHANNEL_ID if to == "channel" else GROUP_ID
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, data=payload)
    return response.status_code == 200