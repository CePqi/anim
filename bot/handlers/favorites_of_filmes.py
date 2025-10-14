from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.core.models import AnimeDao, UserAnimeDao
from bot.keyboards import favorite_keyb, hide_and_delete
from bot.schemas import UserAnimeId

router = Router()


@router.callback_query(F.data == "favorites")
async def get_favorites_films(call: CallbackQuery):
    await call.answer(text="Вкладка для просмотра ваших сохранненых фильмов")
    await call.message.edit_text(
        text="Выберите категорию: ", reply_markup=favorite_keyb()
    )


@router.callback_query(F.data == "your_films")
async def get_user_films(call: CallbackQuery):
    animes = await UserAnimeDao.get_anime_by_user(call.from_user.id)

    await call.answer(text=f"Было найдено {len(animes)} аниме")

    for anime in animes:
        name = anime.anime.name
        episodes = anime.anime.episodes
        year = anime.anime.year
        genre = anime.anime.genre
        rate = anime.anime.rate

        photo = anime.anime.photo_url

        text = (
            f"name: {name}\n"
            f"episodes: {episodes}\n"
            f"year: {year}\n"
            f"genre: {genre}\n"
            f"rate: {rate}\n"
        )
        anime_name = name[:4]
        anime_id = await AnimeDao.get_anime_id_by_name(name=anime_name)
        await call.message.answer_photo(
            photo=photo, caption=text, reply_markup=hide_and_delete(anime_id)
        )


@router.callback_query(F.data.startswith("delete_films_"))
async def delete_films(call: CallbackQuery):
    anime_id = int(call.data.split("_")[2])
    await UserAnimeDao.delete_colum_by_filters(UserAnimeId(anime_id=anime_id))
    await call.message.delete()
    await call.answer(text="Фильм был удален")
