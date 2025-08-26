import os
from binance.client import Client
from dotenv import load_dotenv
from logger import logger

load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

client = Client(
    key=BINANCE_API_KEY,
    secret=BINANCE_API_SECRET,
    base_url="https://testnet.binancefuture.com"  # Futures Testnet
)


def get_balance():
    return 1000  # تغییر در آینده با API واقعی


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
    
    # 1️⃣ ثبت سفارش خرید یا فروش اصلی
    try:
        order = client.new_order(
            symbol=symbol,
            side=order_side,
            type='MARKET',
            quantity=qty
        )
        logger.info(f"✅ سفارش Market با موفقیت ثبت شد: OrderID={order.get('orderId')}")
    except Exception as e:
        logger.exception(f"❌ خطا در ثبت سفارش Market: {e}")
        return

    # 2️⃣ ثبت سفارش TP (Take Profit)
    try:
        tp_order = client.new_order(
            symbol=symbol,
            side=opposite_side,
            type='TAKE_PROFIT_MARKET',
            stopPrice=tp,
            closePosition=True,
            timeInForce="GTC",
            reduceOnly=True,
            workingType="MARK_PRICE"
        )
        logger.info(f"🎯 سفارش TP ثبت شد @ {tp}")
    except Exception as e:
        logger.warning(f"⚠️ ثبت سفارش TP ناموفق: {e}")

    # 3️⃣ ثبت سفارش SL (Stop Loss)
    try:
        sl_order = client.new_order(
            symbol=symbol,
            side=opposite_side,
            type='STOP_MARKET',
            stopPrice=sl,
            closePosition=True,
            timeInForce="GTC",
            reduceOnly=True,
            workingType="MARK_PRICE"
        )
        logger.info(f"🛑 سفارش SL ثبت شد @ {sl}")
    except Exception as e:
        logger.warning(f"⚠️ ثبت سفارش SL ناموفق: {e}")