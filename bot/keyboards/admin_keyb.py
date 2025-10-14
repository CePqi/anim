from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_keyb():
    kb = InlineKeyboardBuilder()

    kb.button(text="Добавить аниме", callback_data="parsing")
    kb.button(text="🔙 Назад в меню", callback_data="menu")

    kb.adjust(1)
    return kb.as_markup()
