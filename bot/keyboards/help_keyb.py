from aiogram.utils.keyboard import InlineKeyboardBuilder


def help_keyb():
    kb = InlineKeyboardBuilder()

    kb.button(
        text="📄 Инструкции (как пользоваться ботом)", callback_data="info_about_bot"
    )
    kb.button(text="🔙 Назад в меню", callback_data="menu")

    kb.adjust(1)
    return kb.as_markup()
