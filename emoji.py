"""Premium-эмодзи для текстов и inline-кнопок.

В тексте:  <tg-emoji emoji-id="...">🔥</tg-emoji>
В кнопке:  InlineKeyboardButton(..., icon_custom_emoji_id="...")
"""


def e(emoji_id: str, fallback: str) -> str:
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'


# === ID эмодзи (получены из стикерпаков) ===
FIRE_ID      = "5424972470023104089"  # огонь
CHECK_ID     = "5206607081334906820"  # галочка
WARN_ID      = "5447644880824181073"  # предупреждение
STAR_ID      = "5438496463044752972"  # звезда
CHART_ID     = "5231200819986047254"  # график
DIAMOND_ID   = "5427168083074628963"  # алмаз
CROWN_ID     = "5217822164362739968"  # корона
GEAR_ID      = "5341715473882955310"  # шестерёнка
BELL_ID      = "5458603043203327669"  # колокол
PARTY_ID     = "5461151367559141950"  # хлопушка
ROCKET_ID    = "5893203503915996356"  # молния (вместо ракеты)
CLOCK_ID     = "5893102202817352158"  # часы
BRIEFCASE_ID = "5893255507380014983"  # портфель
PHONE_ID     = "5893297890117292323"  # звонок (вместо ручки)
BOOK_ID      = "5346132860631791153"  # книга
GLOBE_ID     = "5350747347724810871"  # местоположение (вместо глобуса)
SHIELD_ID    = "5251203410396458957"  # щит
NEW_ID       = "5325547803936572038"  # искры
SUPPORT_ID   = "5443038326535759644"  # чат (поддержка)
FAQ_ID       = "5436113877181941026"  # вопрос
BAN_ID       = "5240241223632954241"  # запрет
SECRET_ID    = "5296369303661067030"  # замок
GUIDE_ID     = None                   # пока Unicode, пришлёшь ID — заменим

# === Готовые строки для текстов ===
FIRE      = e(FIRE_ID, "🔥")
CHECK     = e(CHECK_ID, "✅")
WARN      = e(WARN_ID, "⚠️")
STAR      = e(STAR_ID, "⭐")
CHART     = e(CHART_ID, "📊")
DIAMOND   = e(DIAMOND_ID, "💎")
CROWN     = e(CROWN_ID, "👑")
GEAR      = e(GEAR_ID, "⚙️")
BELL      = e(BELL_ID, "🔔")
PARTY     = e(PARTY_ID, "🎉")
ROCKET    = e(ROCKET_ID, "⚡")
CLOCK     = e(CLOCK_ID, "🕐")
BRIEFCASE = e(BRIEFCASE_ID, "💼")
PHONE     = e(PHONE_ID, "📞")
BOOK      = e(BOOK_ID, "📖")
GLOBE     = e(GLOBE_ID, "📍")
SHIELD    = e(SHIELD_ID, "🛡")
NEW       = e(NEW_ID, "✨")
SUPPORT   = e(SUPPORT_ID, "💬")
FAQ       = e(FAQ_ID, "❓")
BAN       = e(BAN_ID, "🚫")
SECRET    = e(SECRET_ID, "🔒")
GUIDE     = BOOK

# === Заглушки для эмодзи, которых пока нет ===
CROSS  = "❌"
PERSON = "👤"
LOCK   = "🔒"
WALLET = "👛"
