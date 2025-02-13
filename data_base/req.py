### ФАЙЛ ДЛЯ РАБОТЫ ФУНКЦИЙ С МОДЕЛЯМИ БД ###

from sqlalchemy import select
from data_base.struct_1 import async_session # Импортируем функцию асинхронной сессии
from data_base.struct_1 import User,black_list #names, number1 # Импортируем модели из файла struct_1

# Асинхронная функция для добавления пользователя по его tg_id
async def set_user(tg_id: int, name, number): 
       async with async_session() as session: # Создаем асинхронную сессию 
        user = await session.scalar(select(User).where(User.tg_id == tg_id)) # Выполняем запрос для получения ID из таблицы users
        get_name = await session.scalar(select(User).where(User.name == name))
        get_number = await session.scalar(select(User).where(User.number == number))

        if not user and not get_name and not get_number: # Проверяем, существует ли юзер
            session.add(User(tg_id=tg_id, name=name, number=number)) # Если пользователь не найден, добавляем нового пользователя с данным tg_id
            await session.commit() # Сохранение 

async def set_ban(block_tg_id):
    async with async_session() as session:
        get_ban = await session.scalar(select(black_list).where(black_list.block_tg_id == block_tg_id))

        if not get_ban:
            session.add(black_list(block_tg_id=block_tg_id))
            await session.commit()
