# db.py

import sqlite3
from datetime import datetime
from logger import logger
import os

DB_PATH = 'orders.db'

def init_db():
    """ایجاد دیتابیس و جدول 'orders' (در صورت عدم وجود)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        side TEXT NOT NULL,
        entry REAL,
        tp REAL,
        sl REAL,
        qty REAL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()
    logger.info("📦 دیتابیس SQLite آماده‌سازی شد.")


def save_order(symbol, side, entry, tp, sl, qty, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    created_at = datetime.utcnow().isoformat()

    c.execute('''
    INSERT INTO orders (symbol, side, entry, tp, sl, qty, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (symbol, side, entry, tp, sl, qty, status, created_at))

    conn.commit()
    conn.close()
    logger.info(f"💾 سفارش ثبت شد در DB → {symbol} | {side} | {qty} | {status}")