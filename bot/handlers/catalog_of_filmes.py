from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto
from bot.core.models import AnimeDao, UserAnimeDao
from bot.keyboards import (
    catalog_keyb,
    hide_the_message,
    choose_year_keyb,
    choose_rating_keyb,
    next_keyb,
    view_menu_keyb,
)
from bot.schemas import AnimeNews, UserAnimeAdd
import logging
from bot.Fsm import FsmGroup

router = Router()


@router.callback_query(F.data == "catalog")
async def get_catalog_films(call: CallbackQuery):
    await call.answer(text="Здесь можно выбрать фильмы")
    await call.message.edit_text(
        text="Пожалуйста, выберите подходящий вам раздел:", reply_markup=catalog_keyb()
    )


@router.callback_query(F.data == "news")
async def get_news(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    animes = await AnimeDao.get_product_by_filters(AnimeNews(new=True))
    del_animes = []

    await call.answer(text=f"Было найдено {len(animes)} аниме")

    max_len = len(animes)
    await state.update_data(total_row=max_len)

    anime = animes[0]

    del_anime = animes.pop(0)
    del_animes.append(del_anime)

    await state.update_data(animes=animes)
    await state.update_data(del_animes=del_animes)

    text = (
        f"name: {anime.name}\n"
        f"episodes: {anime.episodes}\n"
        f"year: {anime.year}\n"
        f"genre: {anime.genre}\n"
        f"rate: {anime.rate}\n"
    )

    photo_url = anime.photo_url
    await call.message.answer_photo(
        photo=photo_url,
        caption=text,
        reply_markup=hide_the_message(
            anime.id, min_row=len(del_animes), max_row=max_len
        ),
    )

    # else:
    #    await call.message.edit_text(
    #        text="К сожалению на сайте отсутствуют новые аниме"
    #    )


@router.callback_query(F.data == "new_next_anime")
async def get_new_next_anime(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    animes = data.get("animes")
    del_animes = data.get("del_animes")
    max_len = data.get("total_row")

    if len(animes) == 0:
        await call.answer(text="Извините, но больше аниме в данной категории нет")
    else:
        anime = animes[0]

        text = (
            f"name: {anime.name}\n"
            f"episodes: {anime.episodes}\n"
            f"year: {anime.year}\n"
            f"genre: {anime.genre}\n"
            f"rate: {anime.rate}\n"
        )

        photo_url = anime.photo_url

        del_anime = animes.pop(0)
        del_animes.append(del_anime)

        await state.update_data(animes=animes)
        await state.update_data(del_animes=del_animes)

        await call.message.edit_media(
            InputMediaPhoto(media=photo_url, caption=text),
            reply_markup=hide_the_message(
                anime.id, min_row=len(del_animes), max_row=max_len
            ),
        )


@router.callback_query(F.data == "new_previous_anime")
async def get_new_previous_anime(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    animes = data.get("animes")
    del_animes = data.get("del_animes")
    max_len = data.get("total_row")

    if len(del_animes) > 1:

        anime_s = del_animes.pop(-1)
        animes.insert(0, anime_s)

        anime = del_animes[-1]

        text = (
            f"name: {anime.name}\n"
            f"episodes: {anime.episodes}\n"
            f"year: {anime.year}\n"
            f"genre: {anime.genre}\n"
            f"rate: {anime.rate}\n"
        )

        photo_url = anime.photo_url

        await state.update_data(animes=animes)
        await state.update_data(del_animes=del_animes)

        await call.message.edit_media(
            InputMediaPhoto(media=photo_url, caption=text),
            reply_markup=hide_the_message(
                anime.id, min_row=len(del_animes), max_row=max_len
            ),
        )
    else:
        await call.answer(text="Извините, но вы пролистали до первого аниме в списке")


@router.callback_query(F.data.startswith("user_anime_"))
async def add_user_anime(call: CallbackQuery):

    anime_id = int(call.data.split("_")[2])

    user_id = call.from_user.id

    anime = await UserAnimeDao.get_product_by_filters(
        UserAnimeAdd(user_id=user_id, anime_id=anime_id)
    )

    if anime is None:
        await UserAnimeDao.add_table_by_filters(
            UserAnimeAdd(user_id=user_id, anime_id=anime_id)
        )
        logging.info("Аниме было добавлено в список пользователя")
        await call.answer(text="Аниме было добавлено в список пользователя")

    else:
        await call.answer(text="Данное аниме уже состоит в вашем списке")


@router.callback_query(F.data == "search_films")
async def get_search_films(call: CallbackQuery, state: FSMContext):
    await call.answer(text="Здесь можно найти аниме")
    await state.set_state(FsmGroup.year)
    await call.message.edit_text(
        text="Выберите пожалуйста за какой год вы хотите получить аниме: ",
        reply_markup=choose_year_keyb(),
    )


@router.callback_query(F.data.startswith("year_"), FsmGroup.year)
async def get_year(call: CallbackQuery, state: FSMContext):
    year = int(call.data.split("_")[1])
    await state.update_data(year=year)
    await state.set_state(FsmGroup.rating)
    await call.message.edit_text(
        "Напишите рейтинг аниме, напишите целое число",
        reply_markup=choose_rating_keyb(),
    )


@router.callback_query(F.data.startswith("rating_"), FsmGroup.rating)
async def get_rating(call: CallbackQuery, state: FSMContext):
    rating = int(call.data.split("_")[1])

    data = await state.get_data()
    years = data.get("year")

    del_animes = []
    animes = await AnimeDao.get_products_by_year_rate(
        rate_max=float(f"{rating+1}.0"), rate_min=float(f"{rating}.0"), year=years
    )

    if animes is None:
        await call.message.edit_text(
            text="Аниме под вашу категорю не было найдено",
            reply_markup=view_menu_keyb(),
        )
    else:
        max_len = len(animes)
        await state.update_data(total_row=max_len)

        await call.answer(text=f"Было найдено {len(animes)} аниме")

        first_anime = animes[0]
        photo_url = first_anime.photo_url

        text = (
            f"name: {first_anime.name}\n"
            f"episodes: {first_anime.episodes}\n"
            f"year: {first_anime.year}\n"
            f"genre: {first_anime.genre}\n"
            f"rate: {first_anime.rate}\n"
        )

        await call.message.delete()

        del_anime = animes.pop(0)
        del_animes.append(del_anime)

        await state.update_data(animes=animes)
        await state.update_data(del_animes=del_animes)

        await call.message.answer_photo(
            photo=photo_url,
            caption=text,
            reply_markup=next_keyb(
                first_anime.id, min_row=len(del_animes), max_row=max_len
            ),
        )


@router.callback_query(F.data == "next_anime")
async def get_next_anime(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    animes = data.get("animes")
    del_animes = data.get("del_animes")
    max_len = data.get("total_row")

    if len(animes) == 0:
        await call.answer(text="Извините, но больше аниме в данной категории нет")
    else:
        first_anime = animes[0]
        photo_url = first_anime.photo_url

        text = (
            f"name: {first_anime.name}\n"
            f"episodes: {first_anime.episodes}\n"
            f"year: {first_anime.year}\n"
            f"genre: {first_anime.genre}\n"
            f"rate: {first_anime.rate}\n"
        )
        anime_name = first_anime.name[:4]

        del_anime = animes.pop(0)
        del_animes.append(del_anime)

        await state.update_data(animes=animes)
        await call.message.edit_media(
            InputMediaPhoto(media=photo_url, caption=text),
            reply_markup=next_keyb(
                first_anime.id, min_row=len(del_animes), max_row=max_len
            ),
        )


@router.callback_query(F.data == "previous_anime")
async def get_previous_anime(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    animes = data.get("animes")
    del_animes = data.get("del_animes")
    max_len = data.get("total_row")

    if len(del_animes) > 1:

        anime = del_animes.pop(-1)
        animes.insert(0, anime)

        first_anime = del_animes[-1]

        photo_url = first_anime.photo_url

        text = (
            f"name: {first_anime.name}\n"
            f"episodes: {first_anime.episodes}\n"
            f"year: {first_anime.year}\n"
            f"genre: {first_anime.genre}\n"
            f"rate: {first_anime.rate}\n"
        )
        anime_name = first_anime.name[:4]

        await state.update_data(animes=animes)
        await state.update_data(del_animes=del_animes)

        await call.message.edit_media(
            InputMediaPhoto(media=photo_url, caption=text),
            reply_markup=next_keyb(
                first_anime.id, min_row=len(del_animes), max_row=max_len
            ),
        )
    else:
        await call.answer(text="Извините, но вы пролистали до первого аниме в списке")
