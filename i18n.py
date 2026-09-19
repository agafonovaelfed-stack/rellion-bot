"""Локализация: ru / en."""

LANGS = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
}


TEXTS = {
    "ru": {
        "welcome": (
            "<b>Привет!</b>\n\n"
            "Это бот-подборщик заявки.\n"
            "• Выберите тариф\n"
            "• Отлегу аккаунта\n"
            "• Страну\n\n"
            "Затем создайте номер обращения и напишите менеджеру <b>{manager}</b>."
        ),
        "menu_home": "Главное меню.",
        "menu_tariff_title": (
            "<b>Тариф</b> — это срок и объём проверки, "
            "не «качество аккаунта».\nВыберите вариант:"
        ),
        "menu_tips": (
            "<b>Как выбирать:</b>\n\n"
            "<b>Срочный</b> — если важна скорость.\n"
            "<b>Стандарт</b> — если нет жёсткого дедлайна.\n"
            "<b>С проверкой</b> — если хотите меньше сюрпризов.\n\n"
            "<b>Отлега</b> — чем больше лет, тем ниже риск сноса:\n"
            "  5 — база, 6 — уверенно, 7 — высоко, 8 — максимально.\n\n"
            "<b>Страну</b> указывайте ту, которая нужна для вашей задачи."
        ),
        "menu_aging_title": (
            "<b>Выберите отлегу аккаунта</b>\n\n"
            "Чем больше — тем лучше: аккаунт проверен временем "
            "и меньше риск сноса.\nЧем меньше — тем выше риск."
        ),
        "menu_country": "Страна:",
        "draft_title": "<b>Черновик:</b>",
        "draft_tariff": "• тариф: {value}",
        "draft_aging": "• отлега: {value}",
        "draft_country": "• страна: {value}",
        "draft_order": "• заявка: {value}",
        "not_chosen_m": "не выбран",
        "not_chosen_f": "не выбрана",
        "not_yet": "ещё нет",
        "tariff_selected": "<b>{title}</b>\n\n{hint}\n\nДальше выберите страну.",
        "aging_selected": (
            "<b>Отлега: {title}</b>\nКачество: <b>{quality}</b>\n\n"
            "{text}\n\nМожно выбрать страну или создать заявку."
        ),
        "country_selected": (
            "Страна: <b>{country}</b>\n"
            "Тариф: <b>{tariff}</b>\n"
            "Отлега: <b>{aging}</b>\n\nМожно создать заявку."
        ),
        "order_created": (
            "<b>Заявка создана</b>\n\n"
            "<code>{order_id}</code> — {country}, {tariff}, отлега {aging}\n\n"
            "Скопируйте эту строку и напишите {manager}."
        ),
        "need_tariff_country": "Сначала выберите тариф и страну.",
        "btn_tariff": "Выбрать тариф",
        "btn_tips": "Советы по выбору",
        "btn_aging": "Выбор отлеги",
        "btn_country": "Страна",
        "btn_draft": "Моя заявка",
        "btn_manager": "Написать менеджеру",
        "btn_lang": "Язык / Language",
        "btn_back": "Назад",
        "btn_menu": "Меню",
        "btn_home_reply": "🏠 Меню",
        "btn_fast": "Срочный",
        "btn_std": "Стандарт",
        "btn_care": "С проверкой",
        "btn_create_order": "Создать заявку",
        "lang_changed": "Язык переключён на русский.",
        "lang_choose": "Выберите язык / Choose language:",
    },
    "en": {
        "welcome": (
            "<b>Hello!</b>\n\n"
            "This bot helps you prepare a request.\n"
            "• Choose a tariff\n"
            "• Account aging\n"
            "• Country\n\n"
            "Then create a request ID and message the manager <b>{manager}</b>."
        ),
        "menu_home": "Main menu.",
        "menu_tariff_title": (
            "<b>Tariff</b> is about timing and verification level, "
            "not «account quality».\nChoose an option:"
        ),
        "menu_tips": (
            "<b>How to choose:</b>\n\n"
            "<b>Express</b> — if speed matters.\n"
            "<b>Standard</b> — no strict deadline.\n"
            "<b>With check</b> — fewer surprises.\n\n"
            "<b>Aging</b> — the older, the lower the ban risk:\n"
            "  5 — base, 6 — confident, 7 — high, 8 — maximum.\n\n"
            "<b>Country</b> — pick the one needed for your task."
        ),
        "menu_aging_title": (
            "<b>Choose account aging</b>\n\n"
            "The older the better: verified by time, lower ban risk.\n"
            "The newer — the higher the risk."
        ),
        "menu_country": "Country:",
        "draft_title": "<b>Draft:</b>",
        "draft_tariff": "• tariff: {value}",
        "draft_aging": "• aging: {value}",
        "draft_country": "• country: {value}",
        "draft_order": "• request: {value}",
        "not_chosen_m": "not chosen",
        "not_chosen_f": "not chosen",
        "not_yet": "not yet",
        "tariff_selected": "<b>{title}</b>\n\n{hint}\n\nNow choose a country.",
        "aging_selected": (
            "<b>Aging: {title}</b>\nQuality: <b>{quality}</b>\n\n"
            "{text}\n\nYou can pick a country or create a request."
        ),
        "country_selected": (
            "Country: <b>{country}</b>\n"
            "Tariff: <b>{tariff}</b>\n"
            "Aging: <b>{aging}</b>\n\nYou can create a request."
        ),
        "order_created": (
            "<b>Request created</b>\n\n"
            "<code>{order_id}</code> — {country}, {tariff}, aging {aging}\n\n"
            "Copy this line and message {manager}."
        ),
        "need_tariff_country": "Choose tariff and country first.",
        "btn_tariff": "Choose tariff",
        "btn_tips": "Tips",
        "btn_aging": "Choose aging",
        "btn_country": "Country",
        "btn_draft": "My request",
        "btn_manager": "Message manager",
        "btn_lang": "Language / Язык",
        "btn_back": "Back",
        "btn_menu": "Menu",
        "btn_home_reply": "🏠 Menu",
        "btn_fast": "Express",
        "btn_std": "Standard",
        "btn_care": "With check",
        "btn_create_order": "Create request",
        "lang_changed": "Language switched to English.",
        "lang_choose": "Choose language / Выберите язык:",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    """Получить текст по ключу с подстановкой."""
    lang = lang if lang in TEXTS else "ru"
    template = TEXTS[lang].get(key, TEXTS["ru"].get(key, key))
    return template.format(**kwargs) if kwargs else template


# Локализованные названия тарифов и стран
TARIFF_TITLES = {
    "ru": {"fast": "Срочный", "std": "Стандарт", "care": "С проверкой"},
    "en": {"fast": "Express", "std": "Standard", "care": "With check"},
}

TARIFF_HINTS = {
    "ru": {
        "fast": "Быстрее по срокам, меньше проверок на старте.",
        "std": "Баланс цены и срока.",
        "care": "Дольше, но меньше сюрпризов после выдачи.",
    },
    "en": {
        "fast": "Faster timing, fewer initial checks.",
        "std": "Balanced price and timing.",
        "care": "Slower, but fewer surprises after delivery.",
    },
}

AGING_TITLES = {
    "ru": {"5": "5 лет", "6": "6 лет", "7": "7 лет", "8": "8 лет"},
    "en": {"5": "5 years", "6": "6 years", "7": "7 years", "8": "8 years"},
}

AGING_QUALITY = {
    "ru": {"5": "Базовая", "6": "Уверенная", "7": "Высокая", "8": "Максимальная"},
    "en": {"5": "Basic", "6": "Confident", "7": "High", "8": "Maximum"},
}

AGING_TEXT = {
    "ru": {
        "5": "Отлега 5 лет — минимальный порог «выдержанного» аккаунта. Риск сноса умеренный, цена ниже.",
        "6": "Отлега 6 лет — хороший запас времени. Стабильнее, чем 5 лет, риск ниже среднего.",
        "7": "Отлега 7 лет — серьёзный актив. Проверен временем, минимальный риск сноса.",
        "8": "Отлега 8 лет — топовый вариант. Максимальная история, наименьший риск сноса.",
    },
    "en": {
        "5": "5-year aging — minimal threshold of a «seasoned» account. Moderate risk, lower price.",
        "6": "6-year aging — good time reserve. More stable than 5 years, lower-than-average risk.",
        "7": "7-year aging — serious asset. Verified by time, minimal ban risk.",
        "8": "8-year aging — top option. Maximum history, lowest ban risk.",
    },
}

COUNTRY_TITLES = {
    "ru": {
        "ru": "Россия", "kz": "Казахстан", "by": "Беларусь", "ua": "Украина",
        "tr": "Турция", "us": "США", "de": "Германия", "pl": "Польша",
        "gb": "Великобритания", "es": "Испания", "it": "Италия",
        "fr": "Франция", "nl": "Нидерланды", "cz": "Чехия",
        "other": "Другая страна",
    },
    "en": {
        "ru": "Russia", "kz": "Kazakhstan", "by": "Belarus", "ua": "Ukraine",
        "tr": "Turkey", "us": "USA", "de": "Germany", "pl": "Poland",
        "gb": "United Kingdom", "es": "Spain", "it": "Italy",
        "fr": "France", "nl": "Netherlands", "cz": "Czechia",
        "other": "Other country",
    },
}


# === Дополнительные тексты для новых функций ===
EXTRA = {
    "ru": {
        "guide_title": "<b>Что делать после получения аккаунта</b>",
        "guide_text": (
            "1. Сразу смените пароль и привяжите свою почту.\n"
            "2. Включите двухфакторную аутентификацию (2FA).\n"
            "3. Проверьте активные сессии — выкиньте лишние.\n"
            "4. Не входите с одного IP в 10 аккаунтов подряд.\n"
            "5. Первые 2–3 дня не делайте резких действий "
            "(массовых подписок, спама, смены имени).\n"
            "6. Заполните профиль постепенно: аватар, описание, "
            "пара постов — как у живого человека.\n"
            "7. Если что-то пошло не так — сразу пишите менеджеру."
        ),
        "guide_btn": "Гайд после покупки",
        "welcome_first": (
            "<b>Привет! Кажется, ты тут впервые.</b> 👋\n\n"
            "Этот бот помогает оформить заявку на аккаунт:\n"
            "• Выбрать тариф\n"
            "• Определиться с отлегой\n"
            "• Указать нужную страну\n\n"
            "Затем ты получишь номер заявки и сможешь написать менеджеру.\n\n"
            "Пользуйся кнопками ниже — там всё просто."
        ),
        "reply_menu": "Меню",
        "reply_support": "Поддержка",
        "reply_faq": "FAQ",
        "faq_title": "<b>Частые вопросы</b>",
        "faq_text": (
            "<b>1. Это безопасно?</b>\n"
            "Да. Мы не запрашиваем пароли и данные карт. "
            "Все заявки обрабатываются вручную.\n\n"
            "<b>2. Что такое отлега?</b>\n"
            "Это «возраст» аккаунта. Чем больше — тем ниже риск сноса.\n\n"
            "<b>3. Сколько ждать?</b>\n"
            "Зависит от тарифа. Срочный — быстрее всего.\n\n"
            "<b>4. Можно вернуть деньги?</b>\n"
            "Условия обсуждаются с менеджером до оплаты.\n\n"
            "<b>5. Как связаться с менеджером?</b>\n"
            "Кнопка «Написать менеджеру» в главном меню."
        ),
        "support_text": (
            "<b>Поддержка</b>\n\n"
            "Менеджер ответит в рабочее время.\n"
            "Обычно — в течение 15 минут.\n\n"
            "Нажми кнопку ниже, чтобы написать:"
        ),
        "blocked_notice": "(бот заблокирован пользователем)",
        "secret_denied": "⛔ Нет доступа.",
        "secret_welcome": "🔒 Скрытая админ-панель открыта.",
    },
    "en": {
        "guide_title": "<b>What to do after receiving the account</b>",
        "guide_text": (
            "1. Change the password and link your email immediately.\n"
            "2. Enable two-factor authentication (2FA).\n"
            "3. Check active sessions — kick out the extras.\n"
            "4. Don't log into 10 accounts in a row from one IP.\n"
            "5. For the first 2–3 days avoid abrupt actions "
            "(mass follows, spam, renaming).\n"
            "6. Fill the profile gradually: avatar, bio, "
            "a couple of posts — like a real human.\n"
            "7. If something goes wrong — message the manager at once."
        ),
        "guide_btn": "Post-purchase guide",
        "welcome_first": (
            "<b>Hi! Looks like it's your first time here.</b> 👋\n\n"
            "This bot helps you prepare a request for an account:\n"
            "• Choose a tariff\n"
            "• Pick account aging\n"
            "• Specify the country\n\n"
            "Then you'll get a request ID and can message the manager.\n\n"
            "Use the buttons below — it's simple."
        ),
        "reply_menu": "Menu",
        "reply_support": "Support",
        "reply_faq": "FAQ",
        "faq_title": "<b>Frequently asked questions</b>",
        "faq_text": (
            "<b>1. Is it safe?</b>\n"
            "Yes. We don't ask for passwords or card data. "
            "All requests are handled manually.\n\n"
            "<b>2. What is aging?</b>\n"
            "It's the account's «age». The older — the lower the ban risk.\n\n"
            "<b>3. How long does it take?</b>\n"
            "Depends on the tariff. Express is the fastest.\n\n"
            "<b>4. Can I get a refund?</b>\n"
            "Terms are discussed with the manager before payment.\n\n"
            "<b>5. How to contact the manager?</b>\n"
            "Use the «Message manager» button in the main menu."
        ),
        "support_text": (
            "<b>Support</b>\n\n"
            "The manager replies during working hours.\n"
            "Usually within 15 minutes.\n\n"
            "Tap the button below to write:"
        ),
        "blocked_notice": "(bot blocked by user)",
        "secret_denied": "⛔ Access denied.",
        "secret_welcome": "🔒 Hidden admin panel opened.",
    },
}


def tx(lang: str, key: str, **kwargs) -> str:
    """Текст из EXTRA-словаря."""
    lang = lang if lang in EXTRA else "ru"
    template = EXTRA[lang].get(key, EXTRA["ru"].get(key, key))
    return template.format(**kwargs) if kwargs else template
