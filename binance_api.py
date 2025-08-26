import os
from binance.client import Client
from dotenv import load_dotenv
from logger import logger

load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# اتصال به Binance Futures Testnet
client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)
client.FUTURES_URL = "https://testnet.binancefuture.com"
client.API_URL = client.FUTURES_URL

def get_balance():
    return 1000  # بعداً اتصال واقعی به futures_account_balance برمی‌گرده

def calculate_position_size(entry: float, sl: float, risk_percent: float) -> float:
    balance = get_balance()
    risk_amount = balance * (risk_percent / 100)
    sl_distance = abs(entry - sl)

    if sl_distance == 0:
        raise ValueError("SL distance cannot be zero")

    pos_size = risk_amount / sl_distance
    return round(pos_size, 3)

def place_order(symbol, side, qty, entry, tp, sl):
    order_side = 'BUY' if side.lower() == 'buy' else 'SELL'
    opposite_side = 'SELL' if order_side == 'BUY' else 'BUY'

    logger.info(f'📤 ثبت سفارش Market: {order_side} {symbol} Qty={qty}')

    # 1️⃣ سفارش اصلی
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=order_side,
            type='MARKET',
            quantity=qty
        )
        logger.info(f"✅ سفارش Market با موفقیت ثبت شد: OrderID={order.get('orderId')}")
    except Exception as e:
        logger.exception(f"❌ خطا در ثبت سفارش Market: {e}")
        return

    # 2️⃣ سفارش Take Profit
    try:
        tp_order = client.futures_create_order(
            symbol=symbol,
            side=opposite_side,
            type='TAKE_PROFIT_MARKET',
            stopPrice=str(tp),
            closePosition=True,
            timeInForce="GTC",
            reduceOnly=True,
            workingType="MARK_PRICE"
        )
        logger.info(f"🎯 سفارش TP ثبت شد @ {tp}")
    except Exception as e:
        logger.warning(f"⚠️ ثبت سفارش TP ناموفق: {e}")

    # 3️⃣ سفارش Stop Loss
    try:
        sl_order = client.futures_create_order(
            symbol=symbol,
            side=opposite_side,
            type='STOP_MARKET',
            stopPrice=str(sl),
            closePosition=True,
            timeInForce="GTC",
            reduceOnly=True,
            workingType="MARK_PRICE"
        )
        logger.info(f"🛑 سفارش SL ثبت شد @ {sl}")
    except Exception as e:
        logger.warning(f"⚠️ ثبت سفارش SL ناموفق: {e}")