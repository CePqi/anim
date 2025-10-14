from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards import help_keyb, view_menu_keyb

router = Router()


@router.callback_query(F.data == "help_text")
async def help_text(call: CallbackQuery):
    await call.message.edit_text(
        text="Выберите пожалуйста раздел", reply_markup=help_keyb()
    )


@router.callback_query(F.data == "info_about_bot")
async def get_help_message(call: CallbackQuery):
    await call.answer(text="Раздел для обьяснение как работать с ботом")
    text = (
        "❓ <b>Помощь</b>\n\n"
        "Добро пожаловать в бот-каталог фильмов!\n"
        "Вот краткая инструкция по использованию:\n\n"
        "🎞 <b>Каталог фильмов</b>\n"
        "— Просматривайте подборку фильмов, выбирайте жанр и рейтинг, листайте варианты.\n\n"
        "— Для каждого фильма доступны кнопки:\n"
        "Описание — узнать подробности\n"
        "Добавить в избранное — сохранить фильм\n"
        "Скрыть — убрать из списка\n\n"
        "⭐️ <b>Мои избранные</b>\n"
        "— Сохраняйте понравившиеся фильмы\n"
        "— Просматривайте свой список\n"
        "— Удаляйте фильмы из избранного\n\n"
        "📊 <b>Статистика просмотров</b>\n"
        "— Следите за тем, какие фильмы вы добавили за день/неделю\n"
        "— Узнавайте свой любимый жанр\n\n"
        "📄 <b>Инструкции</b>\n"
        "— Подробное руководство по всем функциям\n"
        "— Если возникли вопросы, напишите в поддержку!\n\n"
        "📞 <b>Связь с поддержкой</b>\n"
        "— Мы всегда готовы помочь! Просто напишите свой вопрос."
    )
    await call.message.edit_text(text=text, reply_markup=view_menu_keyb())
