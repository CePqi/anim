from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import settings


def start_keyb(telegram_id: int):
    kb = InlineKeyboardBuilder()

    kb.button(text="🎞 Каталог аниме", callback_data="catalog")
    kb.button(text="⭐️ Мои избранные", callback_data="favorites")
    kb.button(text="📊 Статистика просмотров", callback_data="stats_views")
    kb.button(text="❓ Помощь", callback_data="help_text")
    if telegram_id == settings.ADMIN:
        kb.button(text="Админ панель", callback_data="admin_panel")

    kb.adjust(3)
    return kb.as_markup()
