from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from bot.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool):
        self.engine = create_async_engine(url=url, echo=echo)

        self.factory = async_sessionmaker(
            self.engine, expire_on_commit=False, autocommit=False, autoflush=False
        )

    def get_async_session(self) -> AsyncSession:
        return self.factory()


db_helper = DatabaseHelper(settings.DB_URL, settings.ECHO)
