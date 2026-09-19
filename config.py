"""Конфигурация бота. Все секреты — только через env."""

import os

BOT_TOKEN = os.environ["BOT_TOKEN"]  # обязательно через env
ADMIN_ID = int(os.environ["ADMIN_ID"])  # обязательно через env
MANAGER = os.environ.get("MANAGER", "@vehaus")

DATA_DIR = "data"
DB_PATH = f"{DATA_DIR}/bot.db"
LOG_PATH = f"{DATA_DIR}/logs/bot.log"
EXPORT_DIR = "exports"
LOGO_PATH = "rc.png"

MINI_APP_URL = "https://rellion-bot-1.onrender.com"
