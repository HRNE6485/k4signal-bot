from logger import logger  # ✅ اضافه کن

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")


def send_to_group_and_channel(message: str):
    headers = {"Content-Type": "application/json"}
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "text": message,
        "parse_mode": "Markdown"
    }

    for chat_id in [TELEGRAM_GROUP_ID, TELEGRAM_CHANNEL_ID]:
        payload["chat_id"] = chat_id
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=5)
            if res.ok:
                logger.info(f"📨 پیام به تلگرام ارسال شد → chat_id: {chat_id}")
            else:
                logger.warning(f"⚠️ ارسال پیام به تلگرام ناموفق بود → chat_id: {chat_id} | Code: {res.status_code}")
        except Exception as e:
            logger.exception(f"❌ خطا در ارسال پیام به تلگرام: {e}")