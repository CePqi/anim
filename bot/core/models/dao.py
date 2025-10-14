from datetime import datetime, timedelta
from typing import TypeVar, Type, Generic
import logging
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from . import db_helper
from .base import Base
from sqlalchemy import select, delete, func, cast, String
from typing import TYPE_CHECKING
from .user import User
from .anime import Anime
from .user_anime import UserAnime
from ...schemas import AnimeNews

T = TypeVar("T", bound=Base)


class BaseDao(Generic[T]):
    model: Type[T]

    @classmethod
    async def get_product_by_id(cls, telegram_id: BaseModel):
        async with db_helper.get_async_session() as session:
            logging.info("Получение продукта по айди")
            try:
                exm = select(cls.model).filter_by(
                    **telegram_id.model_dump(exclude_unset=True)
                )
                result = await session.execute(exm)
                user = result.scalar_one_or_none()
                return user

            except SQLAlchemyError as e:
                logging.error(e)

    @classmethod
    async def get_product_by_filters(cls, filters: BaseModel):
        async with db_helper.get_async_session() as session:
            logging.info("Получение продукта по фильтрам")
            try:
                exm = select(cls.model).filter_by(
                    **filters.model_dump(exclude_unset=True)
                )
                result = await session.execute(exm)
                user = result.scalars().all()
                if user:
                    return user
                return None

            except SQLAlchemyError as e:
                logging.error(e)

    @classmethod
    async def add_table_by_filters(cls, filters: BaseModel):
        async with db_helper.get_async_session() as session:
            logging.info(
                f"Добавление новой записи в таблице {cls.model.__name__.lower()}s"
            )
            try:
                upd = session.add(cls.model(**filters.model_dump(exclude_unset=True)))
                await session.commit()
                await session.close()
            except SQLAlchemyError as e:
                logging.error(e)

    @classmethod
    async def delete_colum_by_filters(cls, filters: BaseModel):
        async with db_helper.get_async_session() as session:
            logging.info("Удаление записи")

            exm = delete(cls.model).filter_by(**filters.model_dump(exclude_unset=True))
            await session.execute(exm)
            await session.commit()
            await session.close()


class UserDao(BaseDao[User]):
    model = User

    @classmethod
    async def get_user_and_animes_by_user_id(cls, telegram_id: int):
        async with db_helper.get_async_session() as session:
            logging.info("Получение списка аниме пользователя")

            try:
                exm = (
                    select(User)
                    .options(selectinload(User.animes).selectinload(UserAnime.anime))
                    .where(User.telegram_id == telegram_id)
                )
                result = await session.execute(exm)
                user = result.scalar_one_or_none()
                return user.anime

            except SQLAlchemyError as e:
                logging.error(e)


class AnimeDao(BaseDao[Anime]):
    model = Anime

    @classmethod
    async def get_anime_id_by_name(cls, name: str):
        async with db_helper.get_async_session() as session:
            try:
                exm = select(Anime).where(Anime.name.like(f"{name[:4]}%"))
                result = await session.execute(exm)
                anime = result.scalar_one_or_none()
                return anime.id
            except SQLAlchemyError as e:
                logging.error(e)

    @classmethod
    async def get_products_by_year_rate(
        cls, rate_max: float, rate_min: float, year: int
    ):
        async with db_helper.get_async_session() as session:
            logging.info("Получение продукта по фильтрам")
            try:

                exm = select(cls.model).where(
                    cls.model.year == year,
                    cls.model.rate < rate_max,
                    cls.model.rate >= rate_min,
                )

                result = await session.execute(exm)
                user = result.scalars().all()
                if user:
                    return user
                return None

            except SQLAlchemyError as e:
                logging.error(e)


class UserAnimeDao(BaseDao[UserAnime]):
    model = UserAnime

    @classmethod
    async def get_anime_by_user(cls, user_id: int):
        async with db_helper.get_async_session() as session:
            try:
                logging.info(f"Получение аниме от пользователя {user_id}")
                exm = (
                    select(cls.model)
                    .options(selectinload(cls.model.anime))
                    .where(cls.model.user_id == user_id)
                )
                result = await session.execute(exm)
                animes = result.scalars().all()
                return animes

            except SQLAlchemyError as e:
                logging.error(e)

    @classmethod
    async def get_anime_by_time(cls, days: int, user_id: int):
        async with db_helper.get_async_session() as session:
            logging.info(f"Получение добавлных записей за {days} день(ей)")
            now = datetime.now() - timedelta(days=days)
            exm = select(func.count(cls.model.id).label("total_row_anime")).where(
                cls.model.created_at > now, cls.model.user_id == user_id
            )
            result = await session.execute(exm)
            ani = result.scalar_one_or_none()
            return ani
