"""Логирование в файл + в БД."""

from __future__ import annotations

import logging
import os

from config import LOG_PATH, DATA_DIR
from storage import add_log


def setup_file_logger() -> logging.Logger:
    os.makedirs(f"{DATA_DIR}/logs", exist_ok=True)
    logger = logging.getLogger("bot")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler(LOG_PATH, encoding="utf-8")
        fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(fh)
        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))
        logger.addHandler(sh)
    return logger


log = setup_file_logger()


def event(user_id, username, action, details="") -> None:
    log.info("user=%s @%s action=%s | %s",
             user_id, username or "-", action, details)
    try:
        add_log(user_id, username, action, details)
    except Exception as exc:
        log.exception("failed to write log to DB: %s", exc)
