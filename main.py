### Основной исполняющий файл ### 

import asyncio
import logging
from aiogram import Bot, Dispatcher

from handler import rt # Подключение хендлеров к работе основного файла
from data_base.struct_1 import async_main # Подключение асинхронной функции из файла с моделями БД

# Настраиваем уровень логгирования 
logging.basicConfig(level=logging.INFO)

# Основная асинхронная функция
async def main():
    await async_main() # Вызов асинхронной функции
    bot = Bot(token='7659002618:AAGE2YD9X5CC5mIWO1GQSvxEiaO8g22zb2o') # Инициализация токена
    dp = Dispatcher() # Создание диспетчера
    dp.include_router(rt) # Подключение роутера к диспетчеру
    await dp.start_polling(bot) # Запуск обновлений бота 

# Запуск бота 
if __name__ == "__main__":
    try:
        asyncio.run(main()) # Запуск асинхронной функции 
    except KeyboardInterrupt: # Завершение работы 
        print("В спячку") 
