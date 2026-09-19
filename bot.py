"""Точка входа: пользователь + админ + игры + Secretary Mode."""

from __future__ import annotations

import time

from telegram import Update
from telegram.ext import (
    Application, BusinessConnectionHandler, CallbackQueryHandler,
    CommandHandler, MessageHandler, filters,
)
from telegram.request import HTTPXRequest

from business import (
    on_business_callback, on_business_connection, on_business_message,
)
from config import BOT_TOKEN, ADMIN_ID
from handlers_admin import cmd_admin, on_admin_callback
from handlers_user import cmd_help, cmd_secret, cmd_start, on_callback, on_text
from logger import log
from storage import init_db, set_user_blocked


async def on_error(update: object, context) -> None:
    err = context.error
    log.exception("Exception while handling update:", exc_info=err)

    err_str = repr(err)
    if "bot was blocked" in err_str.lower() or "blocked by the user" in err_str.lower():
        if isinstance(update, Update) and update.effective_user:
            try:
                set_user_blocked(update.effective_user.id, True)
                log.info("User %s blocked the bot", update.effective_user.id)
            except Exception:
                pass

    try:
        if err:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"⚠️ Ошибка в боте:\n<code>{err}</code>",
                parse_mode="HTML",
            )
    except Exception:
        pass


async def on_text_router(update: Update,
                         context: ContextTypes.DEFAULT_TYPE) -> None:
    await on_text(update, context)


def build_app() -> Application:
    request = HTTPXRequest(
        connection_pool_size=8,
        connect_timeout=30.0,
        read_timeout=30.0,
        write_timeout=30.0,
        pool_timeout=30.0,
    )
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .request(request)
        .get_updates_request(request)
        .build()
    )

    # === Secretary Mode ===
    app.add_handler(BusinessConnectionHandler(on_business_connection))
    app.add_handler(MessageHandler(
        filters.UpdateType.BUSINESS_MESSAGE & filters.TEXT & ~filters.COMMAND,
        on_business_message,
    ))

    # === Команды ===
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("admin", cmd_admin))

    # Скрытая админка (//...)
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.Regex(r"^//\w+"),
        cmd_secret,
    ))

    # Команда .play (без слэша)
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.Regex(r"^\.play\b"),
        cmd_play,
    ))

    # === Callback'и ===
    # Business callback'и (игры в бизнес-чате)
    app.add_handler(CallbackQueryHandler(
        on_business_callback,
        pattern=r"^(game_|rps_|coin_|quiz_)",
    ))
    app.add_handler(CallbackQueryHandler(on_admin_callback, pattern=r"^adm_"))
    app.add_handler(CallbackQueryHandler(on_callback))

    # === Текст ===
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        on_text_router,
    ))

    app.add_error_handler(on_error)
    return app


def main() -> None:
    init_db()
    log.info("Bot starting...")

    delay = 5
    while True:
        try:
            app = build_app()
            log.info("Bot polling started.")
            app.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
                close_loop=False,
            )
            break
        except KeyboardInterrupt:
            log.info("Stopped by user (Ctrl+C).")
            break
        except Exception as exc:
            log.warning("Polling crashed: %r. Reconnect in %ss...", exc, delay)
            try:
                time.sleep(delay)
            except KeyboardInterrupt:
                break
            delay = min(delay * 2, 60)


if __name__ == "__main__":
    main()
