from aiogram import Router, F
from aiogram.types import CallbackQuery
from bs4 import BeautifulSoup
import logging
import aiohttp

from bot.core.models import AnimeDao
from bot.keyboards import admin_keyb
from bot.schemas import AnimeName, AnimeUpdate

router = Router()


@router.callback_query(F.data == "admin_panel")
async def admin_panel(call: CallbackQuery):
    await call.answer(text="Вы были допущенны в админ панель")
    await call.message.edit_text(text="Выберите раздел", reply_markup=admin_keyb())


@router.callback_query(F.data == "parsing")
async def parsing_new_anime(call: CallbackQuery):
    for page in range(0, 96, 1):

        url = f"https://animestars.org/page/{page}/"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "lxml")

                logging.info("Парсинг страниц сайта")

                for info in soup.select("div#dle-content > a"):

                    new = False

                    name_tag = info.select_one("div.poster__desc h3")
                    name = name_tag.get_text(strip=True) if name_tag else None
                    list_of_year_genre = info.select_one(
                        "div.poster__meta.flex-grow-1"
                    ).string.split(",")
                    year = list_of_year_genre[0]
                    genre = " ".join(list_of_year_genre[1:])
                    episodes = info.select_one(
                        "div.poster__img div.poster__series"
                    ).next_element.next_element
                    new_har = info.select_one("div.poster__img div.poster__trailer")

                    if "серия" in str(episodes):
                        episode = int(episodes.split(" ")[1])
                    else:
                        episode = episodes.split(" ")[-1]
                        if episode.isdigit():
                            episode = int(episode)
                        else:
                            episode = 0

                    if new_har:
                        new = True

                    rate = float(
                        info.select_one(
                            "div.poster__img div.has-overlay__icon span.poster__ra"
                        ).string
                    )
                    photo_url = (
                        "https://animestars.org/"
                        + info.select_one("div.poster__img img")["src"]
                    )
                    find_anime = await AnimeDao.get_product_by_filters(
                        AnimeName(name=name)
                    )

                    if not find_anime and name != None:
                        logging.info("Добавление аниме в базу данных")
                        await AnimeDao.add_table_by_filters(
                            AnimeUpdate(
                                name=name,
                                episodes=episode,
                                year=int(year),
                                genre=genre,
                                new=new,
                                rate=rate,
                                photo_url=photo_url,
                            )
                        )
                    else:
                        logging.info("Аниме уже было найдено в базе данных")

            await call.answer(text="Сайт был запаршен, новые аниме были добавлены")
