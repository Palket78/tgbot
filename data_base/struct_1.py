### ФАЙЛ С МОДЕЛЯМИ ДЛЯ SQLITE3 ###

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

# Создание асинхронного движка для работы с SQLite базой данных
engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
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

# Модель names с таблицей Имен пользователей
class names(Base):
    __tablename__ = 'names'  # Название таблицы
    id: Mapped[int] = mapped_column(primary_key=True) # Колонка id как первичный ключ
    name = mapped_column(String(36)) # Колонка имя юзера с ограничением в 36 символов

# Модель Number1 с таблицей номеров пользователей 
class number1(Base):
    __tablename__ = 'numbers' # Название таблицы
    id: Mapped[int] = mapped_column(primary_key = True) # Колонка id как первичный ключ
    number = mapped_column(BigInteger) # Определяем колонку number с типом BigInteger

# Асинхронная функция для инициализации БД
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)