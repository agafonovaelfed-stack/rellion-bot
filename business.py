"""Secretary Mode: обработка подключений Business-ботов + игры."""

from __future__ import annotations

from typing import Dict

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import emoji as E
from logger import event

# business_connection_id -> BusinessConnection объект
connections: Dict[str, object] = {}
# chat_id -> business_connection_id
chat_to_conn: Dict[int, str] = {}


async def on_business_connection(update: Update,
                                 context: ContextTypes.DEFAULT_TYPE) -> None:
    conn = update.business_connection
    if not conn:
        return

    if conn.is_enabled:
        connections[conn.id] = conn
        event(conn.user.id, conn.user.username, "business_connected",
              f"conn_id={conn.id}")
        try:
            await context.bot.send_message(
                chat_id=conn.user_chat_id,
                text=(
                    f"{E.CHECK} <b>Secretary Mode подключён!</b>\n\n"
                    f"Теперь бот может отвечать в чатах от твоего имени.\n"
                    f"Напиши <code>.play</code> в любом чате, где бот имеет доступ.\n\n"
                    f"<b>Тестовый режим:</b> ты можешь играть и сам с собой."
                ),
                parse_mode=ParseMode.HTML,
            )
        except Exception:
            pass
    else:
        connections.pop(conn.id, None)
        event(conn.user.id, conn.user.username, "business_disconnected",
              f"conn_id={conn.id}")


async def _get_conn(context: ContextTypes.DEFAULT_TYPE, biz_conn_id: str):
    conn = connections.get(biz_conn_id)
    if conn is None:
        try:
            conn = await context.bot.get_business_connection(biz_conn_id)
            connections[biz_conn_id] = conn
        except Exception:
            return None
    return conn


async def on_business_message(update: Update,
                              context: ContextTypes.DEFAULT_TYPE) -> None:
    """Сообщение в бизнес-чате: .play, числа для игры и т.д."""
    msg = update.business_message
    if not msg or not msg.text:
        return

    biz_conn_id = msg.business_connection_id
    if not biz_conn_id:
        return

    conn = await _get_conn(context, biz_conn_id)
    if not conn:
        return

    chat_to_conn[msg.chat_id] = biz_conn_id

    if not conn.rights or not conn.rights.can_reply:
        return

    text = msg.text.strip()
    # Игры разрешены всем в этом чате (включая владельца)
    sender = msg.from_user
    sender_id = sender.id if sender else None
    sender_name = (sender.first_name if sender else "user") or "user"

    # === .play → открыть меню игр ===
    if text == ".play":
        from games import games_menu_kb
        await context.bot.send_message(
            chat_id=msg.chat_id,
            text=f"{E.PARTY} <b>Мини-игры</b>\n\nВыбери игру:",
            parse_mode=ParseMode.HTML,
            reply_markup=games_menu_kb(),
            business_connection_id=biz_conn_id,
        )
        return

    # === Прочий текст → попробовать как игровой ввод ===
    # (угадай число, ответы на вопросы и т.д.)
    from games import try_business_game_text
    await try_business_game_text(
        context=context,
        chat_id=msg.chat_id,
        user_id=sender_id or 0,
        username=sender_name,
        text=text,
        biz_conn_id=biz_conn_id,
    )


async def on_business_callback(update: Update,
                               context: ContextTypes.DEFAULT_TYPE) -> None:
    """Нажатие inline-кнопки в бизнес-чате."""
    q = update.callback_query
    if not q or not q.data:
        return
    await q.answer()

    msg = q.message
    biz_conn_id = getattr(msg, "business_connection_id", None)
    if not biz_conn_id:
        # fallback: ищем по chat_id
        biz_conn_id = chat_to_conn.get(msg.chat_id)
    if not biz_conn_id:
        return

    conn = await _get_conn(context, biz_conn_id)
    if not conn or not conn.rights or not conn.rights.can_reply:
        return

    from games import handle_business_callback
    await handle_business_callback(
        context=context,
        callback_query=q,
        biz_conn_id=biz_conn_id,
    )
