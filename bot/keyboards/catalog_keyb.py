from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime


def catalog_keyb():
    kb = InlineKeyboardBuilder()

    kb.button(text="🔍 Поиск аниме", callback_data="search_films")
    kb.button(text="📦 Новинки", callback_data="news")
    kb.button(text="🔙 Назад в меню", callback_data="menu")

    kb.adjust(2)
    return kb.as_markup()


def hide_the_message(anime_id, min_row, max_row):
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(text="<=", callback_data="new_previous_anime"),
        InlineKeyboardButton(text="=>", callback_data="new_next_anime"),
    )

    kb.row(InlineKeyboardButton(text=f"{min_row} / {max_row}", callback_data="row"))

    kb.row(
        InlineKeyboardButton(
            text="Добавить в избранное", callback_data=f"user_anime_{anime_id}"
        ),
        InlineKeyboardButton(text="🔙 Назад в меню", callback_data="menu_photo"),
    )

    return kb.as_markup()


def choose_year_keyb():
    kb = InlineKeyboardBuilder()

    now = datetime.now()
    year = now.year

    for i in range(2000, year + 1, 1):
        kb.button(text=str(i), callback_data=f"year_{i}")

    kb.adjust(5)
    return kb.as_markup()


def choose_rating_keyb():
    kb = InlineKeyboardBuilder()

    for i in range(1, 11, 1):
        kb.button(text=str(i), callback_data=f"rating_{i}")

    kb.adjust(3)
    return kb.as_markup()


def next_keyb(anime_name, min_row, max_row):
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(text="<=", callback_data="previous_anime"),
        InlineKeyboardButton(text="=>", callback_data="next_anime"),
    )

    kb.row(InlineKeyboardButton(text=f"{min_row} / {max_row}", callback_data="row"))

    kb.row(
        InlineKeyboardButton(
            text="Добавить в избранное", callback_data=f"user_anime_{anime_name}"
        ),
        InlineKeyboardButton(text="🔙 Назад в меню", callback_data="menu_photo"),
    )

    return kb.as_markup()