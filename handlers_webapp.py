"""Обработка данных из Mini App."""

from __future__ import annotations

import json

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import emoji as E
from config import ADMIN_ID
from logger import event
from storage import create_order


async def on_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Получаем данные от Mini App."""
    user = update.effective_user
    msg = update.effective_message
    if not user or not msg or not msg.web_app_data:
        return

    raw = msg.web_app_data.data
    event(user.id, user.username, "web_app_data", raw[:200])

    try:
        payload = json.loads(raw)
    except Exception:
        await msg.reply_text("⚠️ Не удалось прочитать данные из Mini App.")
        return

    if payload.get("action") != "create_order":
        return

    order_id = payload.get("id") or "—"
    tariff = payload.get("tariff") or "—"
    aging = payload.get("aging") or "—"
    country = payload.get("country") or "—"

    # Сохраняем в БД
    try:
        create_order(
            order_id=order_id,
            user_id=user.id,
            username=user.username,
            tariff=tariff,
            aging=aging,
            country=country,
        )
    except Exception as exc:
        event(user.id, user.username, "web_app_order_error", str(exc))

    # Юзеру
    text = (
        f"{E.CHECK} <b>Заявка {order_id} создана!</b>\n\n"
        f"<b>Тариф:</b> {tariff}\n"
        f"<b>Отлега:</b> {aging}\n"
        f"<b>Страна:</b> {country}\n\n"
        f"Менеджер свяжется с тобой в ближайшее время."
    )
    await msg.reply_text(text, parse_mode=ParseMode.HTML)

    # Тебе в личку
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"🆕 <b>Новая заявка из Mini App</b>\n\n"
                f"<b>ID:</b> {order_id}\n"
                f"<b>Юзер:</b> @{user.username or user.id}\n"
                f"<b>Тариф:</b> {tariff}\n"
                f"<b>Отлега:</b> {aging}\n"
                f"<b>Страна:</b> {country}"
            ),
            parse_mode=ParseMode.HTML,
        )
    except Exception:
        pass
