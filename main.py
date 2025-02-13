### Основной исполняющий файл ### 

import asyncio
import logging

from aiogram import Bot, Dispatcher

from handler import AccessMiddleware, rt # Подключение хендлеров к работе основного файла
from data_base.struct_1 import async_main # Подключение асинхронной функции из файла с моделями БД
from data_base.que_reply import sql_start, close_connection
from keyb import set_main_menu # Подключение быстрого меню
from config_file import config # Подключение функции из конфиг файла

# Настраиваем уровень логгирования 
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value()) # Инициализация токена

# Основная асинхронная функция
async def main():
    await async_main() # Вызов асинхронной функции
    await sql_start()
    dp = Dispatcher() # Создание диспетчера
    dp.message.middleware(AccessMiddleware())
    await set_main_menu(bot) # Вызов быстрого меню 
    dp.include_router(rt) # Подключение роутера к диспетчеру
    await dp.start_polling(bot) # Запуск обновлений бота 

# Запуск бота 
if __name__ == "__main__":
    try:
        asyncio.run(main()) # Запуск асинхронной функции 
    except KeyboardInterrupt: # Завершение работы 
        print("Спать") 
    finally:
        asyncio.run(close_connection())
