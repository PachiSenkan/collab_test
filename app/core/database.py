from typing import Any
from sqlalchemy import JSON
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.config import settings

DATABASE_URL = settings.database_url.unicode_string()  # settings.database_url
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    # pk: Mapped[int] = mapped_column(primary_key=True)
    type_annotation_map = {dict[str, Any]: JSON}
