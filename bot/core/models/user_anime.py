from sqlalchemy import BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from bot.core.models import Base

if TYPE_CHECKING:
    from .user import User
    from .anime import Anime


class UserAnime(Base):
    __tablename__ = "user_anime"

    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.telegram_id"))
    anime_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("animes.id"),
    )

    user: Mapped["User"] = relationship("User", back_populates="animes")
    anime: Mapped["Anime"] = relationship("Anime", back_populates="user_anime")
