"""Пользовательские хендлеры: локализация + гайд + FAQ + поддержка +
автоприветствие + скрытая админка."""

from __future__ import annotations

import random
import string
from pathlib import Path
from typing import Dict

from telegram import (
    InlineKeyboardMarkup, InputFile, Update,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import emoji as E
from config import LOGO_PATH, MANAGER
from i18n import (
    AGING_QUALITY, AGING_TEXT, AGING_TITLES, COUNTRY_TITLES,
    TARIFF_HINTS, TARIFF_TITLES, t, tx,
)
from keyboards import (
    aging_kb, btn, confirm_kb, country_kb, faq_kb, guide_kb,
    lang_kb, main_kb, support_kb, tariff_kb,
)
from logger import event
from storage import (
    create_order, get_user, get_user_lang, set_user_lang,
    set_user_blocked, upsert_user,
)

drafts: Dict[int, Dict[str, str]] = {}
LOGO_ID_CACHE = Path("logo_id.txt")

def get_draft(user_id: int) -> Dict[str, str]:
    return drafts.setdefault(user_id, {})

def new_order_id() -> str:
    letters = "".join(random.choices(string.ascii_uppercase, k=3))
    digits = "".join(random.choices(string.digits, k=4))
    return f"{letters}{digits}"

def _load_logo_id() -> str | None:
    if LOGO_ID_CACHE.exists():
        value = LOGO_ID_CACHE.read_text(encoding="utf-8").strip()
        if value:
            return value
    return None

def _save_logo_id(file_id: str) -> None:
    LOGO_ID_CACHE.write_text(file_id, encoding="utf-8")

async def _send_with_logo(chat_message, text: str, reply_markup=None) -> None:
    file_id = _load_logo_id()
    if file_id:
        try:
            await chat_message.reply_photo(
                photo=file_id, caption=text,
                parse_mode=ParseMode.HTML, reply_markup=reply_markup,
            )
            return
        except Exception:
            LOGO_ID_CACHE.unlink(missing_ok=True)
    logo = Path(LOGO_PATH)
    if not logo.exists():
        await chat_message.reply_text(
            text, parse_mode=ParseMode.HTML, reply_markup=reply_markup,
        )
        return
    with open(logo, "rb") as f:
        photo = InputFile(f, filename=logo.name)
        msg = await chat_message.reply_photo(
            photo=photo, caption=text,
            parse_mode=ParseMode.HTML, reply_markup=reply_markup,
        )
    if msg.photo:
        _save_logo_id(msg.photo[-1].file_id)

async def _render(q, text: str, reply_markup=None) -> None:
    try:
        await q.message.delete()
    except Exception:
        pass
    await _send_with_logo(q.message, text, reply_markup=reply_markup)

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not user or not update.message:
        return
    is_new = get_user(user.id) is None
    upsert_user(user.id, user.username, user.first_name, user.last_name)
    set_user_blocked(user.id, False)
    event(user.id, user.username, "start")
    get_draft(user.id)
    lang = get_user_lang(user.id)

    if is_new:
        text = f"{E.NEW} " + tx(lang, "welcome_first")
    else:
        text = E.PARTY + " " + t(lang, "welcome", manager=MANAGER)

    await _send_with_logo(update.message, text, reply_markup=main_kb(lang))

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    lang = get_user_lang(update.effective_user.id)
    text = f"{E.BOOK} /start — {t(lang, 'menu_home')}"
    await _send_with_logo(update.message, text)

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка reply-кнопок Меню / FAQ / Поддержка."""
    user = update.effective_user
    if not user or not update.message or not update.message.text:
        return
    lang = get_user_lang(user.id)
    txt = (update.message.text or "").strip()

    # Reply-кнопки
    if txt in ("🏠 Меню", "🏠 Menu"):
        await cmd_start(update, context)
        return

    if txt in ("❓ FAQ",):
        await _send_with_logo(
            update.message,
            f"{E.FAQ} " + tx(lang, "faq_title") + "\n\n" + tx(lang, "faq_text"),
            reply_markup=faq_kb(lang),
        )
        return

    if txt in ("🎧 Поддержка", "🎧 Support"):
        await _send_with_logo(
            update.message,
            f"{E.SUPPORT} " + tx(lang, "support_text"),
            reply_markup=support_kb(lang),
        )
        return

    # По умолчанию — открыть главное меню
    await cmd_start(update, context)

async def cmd_secret(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Скрытая админка по кодовому слову."""
    user = update.effective_user
    if not user or not update.message:
        return
    from config import ADMIN_ID
    from keyboards import admin_kb

    text = (update.message.text or "").strip()
    secret_word = "//rellion"  # ← поменяй на своё

    if text.lower() != secret_word:
        return

    lang = get_user_lang(user.id)
    event(user.id, user.username, "secret_attempt", text)

    if user.id != ADMIN_ID:
        await update.message.reply_text(
            tx(lang, "secret_denied"), parse_mode=ParseMode.HTML,
        )
        return

    event(user.id, user.username, "secret_open")
    await update.message.reply_text(
        f"{E.SECRET} " + tx(lang, "secret_welcome") +
        "\n\n" + "🔒 <b>Скрытая админ-панель</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=admin_kb(),
    )

async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    q = update.callback_query
    if not q or not q.from_user or not q.data:
        return
    await q.answer()
    user = q.from_user
    lang = get_user_lang(user.id)
    draft = get_draft(user.id)
    data = q.data

    if not get_user(user.id):
        upsert_user(user.id, user.username, user.first_name, user.last_name)

    event(user.id, user.username, "callback", data)

    if data == "menu_home":
        await _render(
            q,
            f"{E.STAR} {t(lang, 'menu_home')}",
            reply_markup=main_kb(lang),
        )
        return

    if data == "menu_guide":
        await _render(
            q,
            f"{E.GUIDE} " + tx(lang, "guide_title") +
            "\n\n" + tx(lang, "guide_text"),
            reply_markup=guide_kb(lang),
        )
        return

    if data == "menu_faq":
        await _render(
            q,
            f"{E.FAQ} " + tx(lang, "faq_title") + "\n\n" + tx(lang, "faq_text"),
            reply_markup=faq_kb(lang),
        )
        return

    if data == "menu_support":
        await _render(
            q,
            f"{E.SUPPORT} " + tx(lang, "support_text"),
            reply_markup=support_kb(lang),
        )
        return

    if data == "menu_lang":
        await _render(q, t(lang, "lang_choose"), reply_markup=lang_kb())
        return

    if data.startswith("setlang_"):
        new_lang = data.split("_", 1)[1]
        if new_lang in ("ru", "en"):
            set_user_lang(user.id, new_lang)
            event(user.id, user.username, "lang_changed", new_lang)
            lang = new_lang
            await _render(
                q,
                f"{E.CHECK} {t(lang, 'lang_changed')}",
                reply_markup=main_kb(lang),
            )
        return

    if data == "menu_tariff":
        await _render(
            q,
            f"{E.BRIEFCASE} {t(lang, 'menu_tariff_title')}",
            reply_markup=tariff_kb(lang),
        )
        return

    if data == "menu_tips":
        await _render(
            q,
            f"{E.BOOK} {t(lang, 'menu_tips')}",
            reply_markup=main_kb(lang),
        )
        return

    if data == "menu_aging":
        await _render(
            q,
            f"{E.CLOCK} {t(lang, 'menu_aging_title')}",
            reply_markup=aging_kb(lang),
        )
        return

    if data == "menu_country":
        await _render(
            q,
            f"{E.GLOBE} {t(lang, 'menu_country')}",
            reply_markup=country_kb(lang),
        )
        return

    if data == "menu_draft":
        d_tariff = draft.get("tariff_title", t(lang, "not_chosen_m"))
        d_aging = draft.get("aging_title", t(lang, "not_chosen_f"))
        d_country = draft.get("country", t(lang, "not_chosen_f"))
        d_order = draft.get("order_id", t(lang, "not_yet"))
        text = (
            f"{E.BRIEFCASE} {t(lang, 'draft_title')}\n"
            f"{t(lang, 'draft_tariff', value=d_tariff)}\n"
            f"{t(lang, 'draft_aging', value=d_aging)}\n"
            f"{t(lang, 'draft_country', value=d_country)}\n"
            f"{t(lang, 'draft_order', value=d_order)}"
        )
        await _render(q, text, reply_markup=confirm_kb(lang))
        return

    if data.startswith("tariff_"):
        key = data.split("_", 1)[1]
        title = TARIFF_TITLES[lang][key]
        hint = TARIFF_HINTS[lang][key]
        draft["tariff"] = key
        draft["tariff_title"] = title
        await _render(
            q,
            f"{E.CHECK} {t(lang, 'tariff_selected', title=title, hint=hint)}",
            reply_markup=country_kb(lang),
        )
        return

    if data.startswith("aging_"):
        key = data.split("_", 1)[1]
        title = AGING_TITLES[lang][key]
        quality = AGING_QUALITY[lang][key]
        text_body = AGING_TEXT[lang][key]
        draft["aging"] = key
        draft["aging_title"] = title
        draft["aging_quality"] = quality
        await _render(
            q,
            f"{E.CLOCK} " + t(lang, "aging_selected",
                              title=title, quality=quality, text=text_body),
            reply_markup=country_kb(lang),
        )
        return

    if data.startswith("country_"):
        code = data.split("_", 1)[1]
        draft["country"] = COUNTRY_TITLES[lang][code]
        draft["country_code"] = code
        text = t(
            lang, "country_selected",
            country=draft["country"],
            tariff=draft.get("tariff_title", t(lang, "not_chosen_m")),
            aging=draft.get("aging_title", t(lang, "not_chosen_f")),
        )
        await _render(q, f"{E.GLOBE} {text}", reply_markup=confirm_kb(lang))
        return

    if data == "order_create":
        if "tariff_title" not in draft or "country" not in draft:
            await _render(
                q,
                f"{E.WARN} {t(lang, 'need_tariff_country')}",
                reply_markup=main_kb(lang),
            )
            return
        order_id = new_order_id()
        draft["order_id"] = order_id
        aging_part = draft.get("aging_title", "—")
        create_order(
            order_id=order_id, user_id=user.id, username=user.username,
            tariff=draft.get("tariff_title", "—"),
            aging=aging_part,
            country=draft.get("country", "—"),
        )
        event(user.id, user.username, "order_created",
              f"{order_id} | {draft.get('country')} | "
              f"{draft.get('tariff_title')} | aging={aging_part}")

        kb = InlineKeyboardMarkup(
            [
                [btn(t(lang, "btn_manager"),
                     url=f"https://t.me/{MANAGER.lstrip('@')}",
                     style="success", emoji_id=E.PHONE_ID)],
                [btn(t(lang, "btn_menu"), "menu_home")],
            ]
        )
        text = E.BRIEFCASE + " " + t(
            lang, "order_created",
            order_id=order_id,
            country=draft["country"],
            tariff=draft["tariff_title"],
            aging=aging_part,
            manager=MANAGER,
        )
        await _render(q, text, reply_markup=kb)
        return
