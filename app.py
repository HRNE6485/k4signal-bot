# main.py

from flask import Flask, request
from dotenv import load_dotenv
from binance_api import calculate_position_size, place_order
from telegram_bot import send_to_group_and_channel
from logger import logger  # 🚀 اضافه شد!
from db import init_db, save_order

app = Flask(__name__)
load_dotenv()
init_db()


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    try:
        symbol = data['symbol']
        side = data['type']
        entry = float(data['entry'])
        tp = float(data['tp'])
        sl = float(data['sl'])
        risk = float(data.get('risk', 1.0))  # پیش‌فرض 1 درصد ریسک

        logger.info(f"📩 Webhook دریافت شد: {symbol} | {side.upper()} | Entry: {entry} | TP: {tp} | SL: {sl} | Risk: {risk}%")

        qty = calculate_position_size(entry, sl, risk)
        logger.info(f"📏 حجم محاسبه‌شده سفارش: {qty}")

        place_order(symbol, side, qty, entry, tp, sl)

        # بعدش ذخیره در دیتابیس
        save_order(symbol, side, entry, tp, sl, qty, status="OPEN")

        msg = f"""
🚀 سیگنال جدید دریافت شد ({side.upper()}) برای {symbol}

🎯 ورود: `{entry}`
🎯 حد سود: `{tp}`
🛑 حد ضرر: `{sl}`
📊 درصد ریسک: `{risk}%`
📦 حجم سفارش: `{qty}`

#K4SignalBot
"""
        send_to_group_and_channel(msg)
        logger.info("📤 پیام تلگرامی ارسال شد.")

        return "✅ سفارش ثبت شد", 200

    except Exception as e:
        logger.exception(f"❌ خطا در پردازش Webhook: {e}")
        return f"❌ خطا: {str(e)}", 400


if __name__ == '__main__':
    # app.run(port=5000)