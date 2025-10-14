from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.core.models import UserAnimeDao
from bot.keyboards import view_stats_keyb, view_menu_keyb

router = Router()


@router.callback_query(F.data == "stats_views")
async def get_stats_views(call: CallbackQuery):
    await call.answer(text="Здесь можно получить статистику")
    await call.message.edit_text(
        text="Выберить пожалуйста раздел статистики: ", reply_markup=view_stats_keyb()
    )


@router.callback_query(F.data.startswith("films_"))
async def get_films_the_last_day(call: CallbackQuery):
    days = int(call.data.split("_")[1])

    month = "последний месяц"
    if days == 1:
        month = "последний день"
    elif days == 7:
        month = " последнюю неделю"

    total_row = await UserAnimeDao.get_anime_by_time(
        days=days, user_id=call.from_user.id
    )
    await call.message.edit_text(
        text=f"За {month} было добавленно {total_row} аниме в избранное",
        reply_markup=view_menu_keyb(),
    )
