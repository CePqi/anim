from sqlalchemy import TIMESTAMP, func, BIGINT
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=True
    )
