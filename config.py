"""Конфигурация бота. Читает env на Render, fallback — локальные значения."""

import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8759124637:AAEGLit34_Ip_Fb-GHwDFM-PHxW9esxz7B8")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "8933463126"))
MANAGER = os.environ.get("MANAGER", "@vehaus")

DATA_DIR = "data"
DB_PATH = f"{DATA_DIR}/bot.db"
LOG_PATH = f"{DATA_DIR}/logs/bot.log"
EXPORT_DIR = "exports"
LOGO_PATH = "rc.png"
