### ФАЙЛ С МОДЕЛЯМИ ДЛЯ SQLITE3 ###
import datetime

from sqlalchemy import BigInteger, String, DateTime, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

# Создание асинхронного движка для работы с SQLite базой данных
engine = create_async_engine(url=('sqlite+aiosqlite:///db.sqlite3'))
# Создание асинхронной сессии
async_session = async_sessionmaker(engine)

# Базовый класс для определения моделей
class Base(AsyncAttrs, DeclarativeBase):
    pass

# Модель User с таблицей ID пользователей 
class User(Base):
    __tablename__ = 'users' # Название таблицы
    id: Mapped[int] = mapped_column(primary_key=True) # Определяем колонку id как первичный ключ
    tg_id = mapped_column(BigInteger) # Колонка с id юзера
    name = mapped_column(String(36))
    number = mapped_column(BigInteger)

class allow_user(Base):
    __tablename__ = 'allow_users'
    id: Mapped[int] = mapped_column(primary_key=True)
    allow_tg_id = mapped_column(BigInteger)

class black_list(Base):
    __tablename__ = 'blocked'
    id: Mapped[int] = mapped_column(primary_key=True)
    block_tg_id = mapped_column(BigInteger)

# Асинхронная функция для инициализации БД
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)