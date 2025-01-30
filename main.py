### Основной исполняющий файл ### 

import asyncio
import logging
from aiogram import Bot, Dispatcher

from handler import rt # Подключение хендлеров к работе основного файла
from data_base.struct_1 import async_main # Подключение асинхронной функции из файла с моделями БД
from keyb import set_main_menu # Подключение быстрого меню
from config_file import config # Подключение функции из конфиг файла

# Настраиваем уровень логгирования 
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value()) # Инициализация токена

# Основная асинхронная функция
async def main():
    await async_main() # Вызов асинхронной функции
    dp = Dispatcher() # Создание диспетчера
    await set_main_menu(bot) # Вызов быстрого меню 
    dp.include_router(rt) # Подключение роутера к диспетчеру
    await dp.start_polling(bot) # Запуск обновлений бота 

# Запуск бота 
if __name__ == "__main__":
    try:
        asyncio.run(main()) # Запуск асинхронной функции 
    except KeyboardInterrupt: # Завершение работы 
        print("Спать") 
