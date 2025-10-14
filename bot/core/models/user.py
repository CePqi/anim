from sqlalchemy import BIGINT, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .user_anime import UserAnime


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    first_name: Mapped[str] = mapped_column(TEXT)
    last_name: Mapped[str | None]
    username: Mapped[str] = mapped_column(TEXT, unique=True)

    animes: Mapped[list["UserAnime"]] = relationship(
        "UserAnime", back_populates="user", cascade="all, delete-orphan"
    )
