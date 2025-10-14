from pydantic import BaseModel


class TelegramID(BaseModel):
    telegram_id: int


class UserUpdate(BaseModel):
    telegram_id: int
    first_name: str
    last_name: str | None
    username: str


class AnimeUpdate(BaseModel):
    name: str
    episodes: int
    year: int
    genre: str
    new: bool
    rate: float
    photo_url: str


class AnimeName(BaseModel):
    name: str


class AnimeRateYear(BaseModel):
    rate: int
    year: int


class AnimeNews(BaseModel):
    new: bool


class UserAnimeAdd(BaseModel):
    user_id: int
    anime_id: int


class UserAnimeId(BaseModel):
    anime_id: int
