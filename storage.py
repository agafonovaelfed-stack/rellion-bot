"""SQLite: пользователи, заявки, логи."""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from typing import Iterable

from config import DB_PATH, DATA_DIR


def _ensure_dirs() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(f"{DATA_DIR}/logs", exist_ok=True)


def _connect() -> sqlite3.Connection:
    _ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY,
                username    TEXT,
                first_name  TEXT,
                last_name   TEXT,
                first_seen  TEXT NOT NULL,
                last_seen   TEXT NOT NULL,
                is_blocked  INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS orders (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id    TEXT UNIQUE NOT NULL,
                user_id     INTEGER NOT NULL,
                username    TEXT,
                tariff      TEXT,
                aging       TEXT,
                country     TEXT,
                created_at  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS logs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                ts          TEXT NOT NULL,
                user_id     INTEGER,
                username    TEXT,
                action      TEXT NOT NULL,
                details     TEXT
            );
            """
        )


def upsert_user(user_id, username, first_name, last_name) -> None:
    now = datetime.utcnow().isoformat(timespec="seconds")
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO users (user_id, username, first_name, last_name,
                               first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username   = excluded.username,
                first_name = excluded.first_name,
                last_name  = excluded.last_name,
                last_seen  = excluded.last_seen
            """,
            (user_id, username, first_name, last_name, now, now),
        )


def get_user(user_id):
    with _connect() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()


def count_users() -> int:
    with _connect() as conn:
        return conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]


def list_users(limit=50, offset=0):
    with _connect() as conn:
        return conn.execute(
            "SELECT * FROM users ORDER BY last_seen DESC LIMIT ? OFFSET ?",
            (limit, offset),
        ).fetchall()


def create_order(order_id, user_id, username, tariff, aging, country) -> None:
    now = datetime.utcnow().isoformat(timespec="seconds")
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO orders (order_id, user_id, username,
                                tariff, aging, country, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (order_id, user_id, username, tariff, aging, country, now),
        )


def count_orders() -> int:
    with _connect() as conn:
        return conn.execute("SELECT COUNT(*) AS c FROM orders").fetchone()["c"]


def list_orders(limit=50, offset=0):
    with _connect() as conn:
        return conn.execute(
            "SELECT * FROM orders ORDER BY id DESC LIMIT ? OFFSET ?",
            (limit, offset),
        ).fetchall()


def add_log(user_id, username, action, details="") -> None:
    now = datetime.utcnow().isoformat(timespec="seconds")
    with _connect() as conn:
        conn.execute(
            "INSERT INTO logs (ts, user_id, username, action, details) "
            "VALUES (?, ?, ?, ?, ?)",
            (now, user_id, username, action, details),
        )


def count_logs() -> int:
    with _connect() as conn:
        return conn.execute("SELECT COUNT(*) AS c FROM logs").fetchone()["c"]


def all_logs() -> Iterable:
    with _connect() as conn:
        return conn.execute("SELECT * FROM logs ORDER BY id ASC").fetchall()


def export_logs_to_txt(path: str) -> int:
    rows = list(all_logs())
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Export logs — {datetime.utcnow().isoformat()}Z\n")
        f.write(f"# Total: {len(rows)}\n\n")
        for r in rows:
            f.write(
                f"[{r['ts']}] user={r['user_id']} (@{r['username'] or '-'}) "
                f"action={r['action']} | {r['details'] or ''}\n"
            )
    return len(rows)


def get_user_lang(user_id: int) -> str:
    """Получить язык пользователя (ru/en). По умолчанию ru."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT lang FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return (row["lang"] if row and row["lang"] else "ru")


def set_user_lang(user_id: int, lang: str) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE users SET lang = ? WHERE user_id = ?",
            (lang, user_id),
        )


def set_user_blocked(user_id: int, blocked: bool) -> None:
    """Пометить пользователя как заблокированного."""
    with _connect() as conn:
        conn.execute(
            "UPDATE users SET is_blocked = ? WHERE user_id = ?",
            (1 if blocked else 0, user_id),
        )


def all_user_ids() -> list[int]:
    """Все id пользователей (для рассылок и проверок)."""
    with _connect() as conn:
        rows = conn.execute("SELECT user_id FROM users").fetchall()
        return [r["user_id"] for r in rows]
