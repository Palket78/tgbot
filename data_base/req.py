### ФАЙЛ ДЛЯ РАБОТЫ ФУНКЦИЙ С МОДЕЛЯМИ БД ###

from data_base.struct_1 import async_session # Импортируем функцию асинхронной сессии
from data_base.struct_1 import User, names, number1 # Импортируем модели из файла struct_1
from sqlalchemy import select

# Асинхронная функция для добавления пользователя по его tg_id
async def set_user(tg_id: int): 
       async with async_session() as session: # Создаем асинхронную сессию 
        user = await session.scalar(select(User).where(User.tg_id == tg_id)) # Выполняем запрос для получения ID из таблицы users

        if not user: # Проверяем, существует ли юзер
            session.add(User(tg_id=tg_id)) # Если пользователь не найден, добавляем нового пользователя с данным tg_id
            await session.commit() # Сохранение 

# Асинхронная функция для добавления имени
async def set_name(name):
    async with async_session() as session: # Создаем асинхронную сессию
        get_name = await session.scalar(select(names).where(names.name == name))  # Выполняем запрос для получения имени из таблицы names

        if not get_name: # Проверяем, существует ли имя
            session.add(names(name=name)) # Если нет, то вносим в таблицу
            await session.commit() # Сохраняем

# Асинхронная функция для добавления номера
async def set_number(number):
    async with async_session() as session: # Создаем асинх.сесси.
        get_number = await session.scalar(select(number1).where(number1.number == number)) # Выполняем запрос для получения номера из таблицы numbers

        if not get_number: # Проверяем, существует ли номер
            session.add(number1(number=number)) # Если нет вносим в таблицу
            await session.commit() # Сохраняем

