from sqlalchemy import BIGINT, TEXT, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .user_anime import UserAnime


class Anime(Base):
    __tablename__ = "animes"

    name: Mapped[str] = mapped_column(TEXT, nullable=False, unique=True)
    episodes: Mapped[int] = mapped_column(BIGINT, nullable=False)
    year: Mapped[int] = mapped_column(BIGINT, nullable=False)
    genre: Mapped[str] = mapped_column(TEXT, nullable=False)
    new: Mapped[bool] = mapped_column(Boolean)
    rate: Mapped[float] = mapped_column(Float, nullable=False)
    photo_url: Mapped[str] = mapped_column(TEXT, nullable=False, unique=True)

    user_anime: Mapped[list["UserAnime"]] = relationship(
        "UserAnime", back_populates="anime", cascade="all, delete-orphan"
    )
