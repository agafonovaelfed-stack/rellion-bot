"""Админ-панель."""

from __future__ import annotations

import os
from datetime import datetime

from telegram import InputFile, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import emoji as E
from config import ADMIN_ID, EXPORT_DIR
from keyboards import admin_back_kb, admin_kb
from logger import event
from storage import (
    all_logs, count_logs, count_orders, count_users,
    export_logs_to_txt, list_orders, list_users,
)


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


async def cmd_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not user or not update.message:
        return
    if not is_admin(user.id):
        await update.message.reply_text("⛔ Нет доступа.")
        event(user.id, user.username, "admin_denied")
        return
    event(user.id, user.username, "admin_open")
    await update.message.reply_text(
        f"{E.GEAR} <b>Админ-панель</b>\n\nВыбери раздел:",
        parse_mode=ParseMode.HTML,
        reply_markup=admin_kb(),
    )


async def on_admin_callback(update: Update,
                            context: ContextTypes.DEFAULT_TYPE) -> None:
    q = update.callback_query
    if not q or not q.from_user or not q.data:
        return
    await q.answer()
    user = q.from_user
    if not is_admin(user.id):
        return
    data = q.data

    if data == "adm_home":
        await q.edit_message_text(
            f"{E.GEAR} <b>Админ-панель</b>\n\nВыбери раздел:",
            parse_mode=ParseMode.HTML,
            reply_markup=admin_kb(),
        )
        return

    if data == "adm_stats":
        event(user.id, user.username, "admin_stats")
        text = (
            f"{E.CHART} <b>Статистика</b>\n\n"
            f"{E.PERSON} Пользователей: <b>{count_users()}</b>\n"
            f"{E.PACKAGE} Заявок: <b>{count_orders()}</b>\n"
            f"{E.BOOK} Записей в логах: <b>{count_logs()}</b>"
        )
        await q.edit_message_text(
            text, parse_mode=ParseMode.HTML, reply_markup=admin_back_kb(),
        )
        return

    if data == "adm_orders":
        event(user.id, user.username, "admin_orders")
        rows = list_orders(limit=20)
        if not rows:
            text = f"{E.PACKAGE} Заявок пока нет."
        else:
            lines = [f"{E.PACKAGE} <b>Последние заявки:</b>\n"]
            for r in rows:
                lines.append(
                    f"<code>{r['order_id']}</code> — "
                    f"{r['country']}, {r['tariff']}, отлега {r['aging']}\n"
                    f"   от @{r['username'] or r['user_id']} • {r['created_at']}"
                )
            text = "\n".join(lines)
        await q.edit_message_text(
            text, parse_mode=ParseMode.HTML, reply_markup=admin_back_kb(),
        )
        return

    if data == "adm_users":
        event(user.id, user.username, "admin_users")
        rows = list_users(limit=20)
        if not rows:
            text = f"{E.PERSON} Пользователей пока нет."
        else:
            lines = [f"{E.PERSON} <b>Последние пользователи:</b>\n"]
            for r in rows:
                lines.append(
                    f"• <b>{r['first_name'] or '-'}</b> "
                    f"(@{r['username'] or '-'}, id <code>{r['user_id']}</code>)\n"
                    f"   первый: {r['first_seen']}, последний: {r['last_seen']}"
                )
            text = "\n".join(lines)
        await q.edit_message_text(
            text, parse_mode=ParseMode.HTML, reply_markup=admin_back_kb(),
        )
        return

    if data == "adm_logs_show":
        event(user.id, user.username, "admin_logs_show")
        logs = list(all_logs())[-20:]
        if not logs:
            text = f"{E.BOOK} Логов пока нет."
        else:
            lines = [f"{E.BOOK} <b>Последние 20 логов:</b>\n"]
            for r in logs:
                lines.append(
                    f"<code>{r['ts']}</code> | "
                    f"{r['user_id']} (@{r['username'] or '-'}) | "
                    f"{r['action']} | {r['details'] or ''}"
                )
            text = "\n".join(lines)
        await q.edit_message_text(
            text, parse_mode=ParseMode.HTML, reply_markup=admin_back_kb(),
        )
        return

    if data == "adm_logs_export":
        event(user.id, user.username, "admin_logs_export")
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"logs_{ts}.txt"
        path = os.path.join(EXPORT_DIR, filename)
        n = export_logs_to_txt(path)
        await q.edit_message_text(
            f"{E.CHECK} Готовлю файл ({n} строк)...",
            parse_mode=ParseMode.HTML,
        )
        with open(path, "rb") as f:
            await q.message.reply_document(
                document=InputFile(f, filename=filename),
                caption=f"{E.BOOK} Логи: {n} записей",
                parse_mode=ParseMode.HTML,
            )
        return
