from flask import Flask, request, jsonify
from telegram_bot import send_telegram_message
from binance_api import send_order

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "K4 Signal Webhook is Running 🚀"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        symbol = data['symbol']
        signal_type = data['type']  # buy or sell
        entry = data['entry']
        sl = data.get('sl')
        tp = data.get('tp')
        risk = data.get('risk', 1)

        # مقدار حجم فرضی برای تست (بر حسب ریاضی می‌تونیم بعداً اصلاح کنیم)
        quantity = 0.01  

        signal_text = f"""
📡 *سیگنال جدید K4Signal*
🪙 *نماد:* `{symbol}`
📥 *نوع سیگنال:* {signal_type.upper()}
🎯 *قیمت ورود:* {entry}
💰 *TP:* {tp or '---'}  |  🛡️ *SL:* {sl or '---'}
📊 *ریسک تخمینی:* {risk}٪
"""

        send_telegram_message(signal_text, to="channel")
        send_telegram_message(signal_text, to="group")

        binance_result = send_order(symbol, signal_type, quantity, sl=sl, tp=tp)

        if binance_result["status"] == "success":
            return jsonify({"status": "ok", "binance_result": binance_result}), 200
        else:
            return jsonify({"status": "error", "message": "Order failed", "detail": binance_result}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)