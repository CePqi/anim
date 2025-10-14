from aiogram.utils.keyboard import InlineKeyboardBuilder


def favorite_keyb():
    kb = InlineKeyboardBuilder()

    kb.button(text="📜 Список фильмов", callback_data="your_films")
    kb.button(text="🔙 Назад в меню", callback_data="menu")

    kb.adjust(1)
    return kb.as_markup()


def hide_and_delete(name: str):
    kb = InlineKeyboardBuilder()

    kb.button(text="🗑 Удалить из избранного", callback_data=f"delete_films_{name}")
    kb.button(text="Скрыть сообщение", callback_data="delete_message")

    kb.adjust(1)
    return kb.as_markup()
