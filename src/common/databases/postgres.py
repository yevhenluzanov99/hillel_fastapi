import logging
from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import declarative_base

from src.base_settings import PostgresSettings

logger = logging.getLogger(__name__)

Base = declarative_base()

class Database:
    def __init__(self):
        self.__session = None
        self.__engine: Optional[AsyncEngine] = None

    def connect(self, db_conf: PostgresSettings):
        self.__engine = create_async_engine(db_conf.url)
        self.__session = async_sessionmaker(
            bind=self.__engine,
            autocommit=False,
        )

    async def disconnect(self):
        await self.__engine.dispose()


    def get_engine(self) -> AsyncEngine:
        return self.__engine

    async def get_db(self):
        async with self.__session() as session:
            yield session



postgres = Database()

async def get_session():
    async for session in postgres.get_db():
        yield session