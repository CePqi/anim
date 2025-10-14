from aiogram.utils.keyboard import InlineKeyboardBuilder


def view_stats_keyb():
    kb = InlineKeyboardBuilder()

    kb.button(text="📅 Фильмы, добавленные за день", callback_data="films_1")
    kb.button(text="📆 Фильмы, добавленные за неделю", callback_data="films_7")
    kb.button(text="📆 Фильмы, добавленные за месяц", callback_data="films_30")
    kb.button(text="🔙 Назад в меню", callback_data="menu")

    kb.adjust(1)
    return kb.as_markup()


def view_menu_keyb():
    kb = InlineKeyboardBuilder()

    kb.button(text="🔙 Назад в меню", callback_data="menu")

    kb.adjust(1)
    return kb.as_markup()
