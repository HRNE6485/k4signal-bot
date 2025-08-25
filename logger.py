# logger.py

import logging
from logging.handlers import RotatingFileHandler
import os
import sys

LOGGER_NAME = "K4SignalBot"
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)

if not logger.handlers:

    # 📂 پوشه لاگ
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # 📁 فایل لاگ
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=5 * 1024 * 1024, backupCount=5)
    file_format = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    file_handler.setFormatter(file_format)

    # 🖥 کنسول هندلر با UTF-8 safe ویندوزی
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_format = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    console_handler.setFormatter(console_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)