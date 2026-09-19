"""Все inline-клавиатуры с локализацией и Premium-эмодзи.
Reply-кнопок нет вообще."""

from __future__ import annotations

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import emoji as E
from config import MANAGER
from i18n import (
    AGING_TITLES, COUNTRY_TITLES, LANGS, TARIFF_TITLES, t, tx,
)


def btn(text, callback_data=None, url=None,
        style=None, emoji_id=None) -> InlineKeyboardButton:
    kwargs = {"text": text}
    if callback_data is not None:
        kwargs["callback_data"] = callback_data
    if url is not None:
        kwargs["url"] = url
    if style is not None:
        kwargs["style"] = style
    if emoji_id is not None:
        try:
            return InlineKeyboardButton(**kwargs, icon_custom_emoji_id=emoji_id)
        except TypeError:
            pass
    try:
        return InlineKeyboardButton(**kwargs)
    except TypeError:
        kwargs.pop("style", None)
        return InlineKeyboardButton(**kwargs)


def main_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [btn(t(lang, "btn_tariff"), "menu_tariff",
                 style="success", emoji_id=E.BRIEFCASE_ID)],
            [btn(t(lang, "btn_tips"), "menu_tips",
                 style="primary", emoji_id=E.BOOK_ID)],
            [btn(t(lang, "btn_aging"), "menu_aging",
                 style="primary", emoji_id=E.CLOCK_ID)],
            [btn(t(lang, "btn_country"), "menu_country",
                 style="primary", emoji_id=E.GLOBE_ID)],
            [btn(t(lang, "btn_draft"), "menu_draft",
                 style="primary", emoji_id=E.CHECK_ID)],
            [btn(tx(lang, "guide_btn"), "menu_guide",
                 style="success", emoji_id=E.BOOK_ID)],
            [btn(tx(lang, "reply_faq"), "menu_faq",
                 style="primary", emoji_id=E.FAQ_ID)],
            [btn(tx(lang, "reply_support"), "menu_support",
                 style="primary", emoji_id=E.SUPPORT_ID)],
            [btn(t(lang, "btn_lang"), "menu_lang",
                 style="primary")],
            [btn(t(lang, "btn_manager"),
                 url=f"https://t.me/{MANAGER.lstrip('@')}",
                 style="danger", emoji_id=E.PHONE_ID)],
        ]
    )


def lang_kb() -> InlineKeyboardMarkup:
    rows = [
        [btn(label, f"setlang_{code}", style="primary")]
        for code, label in LANGS.items()
    ]
    rows.append([btn("← Menu", "menu_home")])
    return InlineKeyboardMarkup(rows)


def tariff_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [btn(TARIFF_TITLES[lang]["fast"], "tariff_fast",
                 style="danger", emoji_id=E.ROCKET_ID)],
            [btn(TARIFF_TITLES[lang]["std"], "tariff_std",
                 style="primary", emoji_id=E.CHART_ID)],
            [btn(TARIFF_TITLES[lang]["care"], "tariff_care",
                 style="success", emoji_id=E.SHIELD_ID)],
            [btn(t(lang, "btn_back"), "menu_home")],
        ]
    )


def aging_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [btn(AGING_TITLES[lang]["5"], "aging_5",
                 style="danger", emoji_id=E.CLOCK_ID)],
            [btn(AGING_TITLES[lang]["6"], "aging_6",
                 style="primary", emoji_id=E.CLOCK_ID)],
            [btn(AGING_TITLES[lang]["7"], "aging_7",
                 style="success", emoji_id=E.CLOCK_ID)],
            [btn(AGING_TITLES[lang]["8"], "aging_8",
                 style="success", emoji_id=E.CROWN_ID)],
            [btn(t(lang, "btn_back"), "menu_home")],
        ]
    )


def country_kb(lang: str) -> InlineKeyboardMarkup:
    rows = [
        [btn(name, f"country_{code}",
             style="primary", emoji_id=E.GLOBE_ID)]
        for code, name in COUNTRY_TITLES[lang].items()
    ]
    rows.append([btn(t(lang, "btn_back"), "menu_home")])
    return InlineKeyboardMarkup(rows)


def confirm_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [btn(t(lang, "btn_create_order"), "order_create",
                 style="success", emoji_id=E.CHECK_ID)],
            [btn(t(lang, "btn_menu"), "menu_home")],
        ]
    )


def faq_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [btn(tx(lang, "reply_support"), "menu_support",
                 style="success", emoji_id=E.SUPPORT_ID)],
            [btn(t(lang, "btn_manager"),
                 url=f"https://t.me/{MANAGER.lstrip('@')}",
                 style="danger", emoji_id=E.PHONE_ID)],
            [btn(t(lang, "btn_back"), "menu_home")],
        ]
    )


def support_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [btn(t(lang, "btn_manager"),
                 url=f"https://t.me/{MANAGER.lstrip('@')}",
                 style="success", emoji_id=E.PHONE_ID)],
            [btn(t(lang, "btn_back"), "menu_home")],
        ]
    )


def guide_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[btn(t(lang, "btn_menu"), "menu_home")]]
    )


def admin_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [btn("Статистика", "adm_stats",
                 style="primary", emoji_id=E.CHART_ID)],
            [btn("Заявки", "adm_orders",
                 style="primary", emoji_id=E.BRIEFCASE_ID)],
            [btn("Пользователи", "adm_users",
                 style="primary", emoji_id=E.STAR_ID)],
            [btn("Логи в TXT", "adm_logs_export",
                 style="success", emoji_id=E.CHECK_ID)],
            [btn("Логи (последние 20)", "adm_logs_show",
                 style="primary", emoji_id=E.BOOK_ID)],
            [btn("Меню пользователя", "menu_home",
                 style="danger", emoji_id=E.WARN_ID)],
        ]
    )


def admin_back_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[btn("Назад в админку", "adm_home",
              style="primary", emoji_id=E.GEAR_ID)]]
    )
