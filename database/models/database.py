from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import String, Boolean, Integer, TIMESTAMP, ForeignKey, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from models import Users

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# class Users(SQLAlchemyBaseUserTable[int], Base):
#
#     id: Mapped[int] = mapped_column(
#         Integer, primary_key=True
#     )
#     email: Mapped[str] = mapped_column(
#         String(length=320), unique=True, index=True, nullable=False
#     )
#     username: Mapped[str] = mapped_column(
#         String, nullable=False
#     )
#     registered_at: Mapped[TIMESTAMP] = mapped_column(
#         TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
#     )
#     role_id: Mapped[int] = mapped_column(
#         Integer, ForeignKey("role.id")
#     )
#     hashed_password: Mapped[str] = mapped_column(
#         String(length=1024), nullable=False
#     )
#     is_active: Mapped[bool] = mapped_column(
#         Boolean, default=True, nullable=False
#     )
#     is_superuser: Mapped[bool] = mapped_column(
#         Boolean, default=False, nullable=False
#     )
#     is_verified: Mapped[bool] = mapped_column(
#         Boolean, default=False, nullable=False
#     )


engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, Users)
