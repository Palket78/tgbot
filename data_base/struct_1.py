### ФАЙЛ С МОДЕЛЯМИ ДЛЯ SQLITE3 ###

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config_file import config

# Создание асинхронного движка для работы с SQLite базой данных
engine = create_async_engine(url=(config.sql_url))
# Создание асинхронной сессии
async_session = async_sessionmaker(engine)

# Базовый класс для определения моделей
class Base(AsyncAttrs, DeclarativeBase):
    pass

# Таблица Users с наследованием от класса Base
class User(Base):
    __tablename__ = 'users' # Название таблицы
    id: Mapped[int] = mapped_column(primary_key=True) # Определяем колонку id как первичный ключ
    tg_id = mapped_column(BigInteger) # Колонка с id юзера
    name = mapped_column(String(36)) # Колонка с введеным именем юзера
    number = mapped_column(BigInteger) # Колонка с контактом юзера

# Таблица вайтлиста с наследованием от класса Base
class allow_user(Base):
    __tablename__ = 'allow_users' # Название таблицы
    id: Mapped[int] = mapped_column(primary_key=True) # Определение колонки идентификатора записи
    allow_tg_id = mapped_column(BigInteger) # колонка с id юзера

# Таблица блеклиста с наследованием от класса Base
class black_list(Base):
    __tablename__ = 'blocked' # Название таблицы 
    id: Mapped[int] = mapped_column(primary_key=True) # Определение колонки идентификатора записи
    block_tg_id = mapped_column(BigInteger) # колонка с id юзера

# Асинхронная функция для инициализации БД
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)