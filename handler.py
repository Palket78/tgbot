### Файл с реализацией хендлеров ###

from aiogram import types
from aiogram.types import Message
from aiogram.filters.command import Command, CommandStart
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import sqlite3

import keyb as keyboard # Импортируем файл с кнопками
import texts as txt # Импортируем файл с текстами
import data_base.req as rq # Подключаем файл с реализацией функций внесесения пользователей в БД

rt = Router() # Отделяем файл с хендлерами от остальных модулей

# Класс регистрации пользователя по параметрам: Имя, Номер телефона
class Register(StatesGroup):
    name = State()
    number = State()

# Обработчик для команды /start
@rt.message(CommandStart())
async def cmd_start(message: types.Message):
    con = sqlite3.connect("db.sqlite3") # Подключение к базе данных SQLite3
    cursor = con.cursor() # Создаем курсор для выполнения SQL запросов
    cursor.execute(f"SELECT tg_id FROM users WHERE tg_id = {message.from_user.id}")  # Запрос для проверки, существует ли пользователь в базе данных по его TG_ID
    user_id_massive = cursor.fetchall()
    txt_3 = txt.text_3 # Текст главного меню
    if user_id_massive: # Если пользователь найден, отправляем сообщение главного меню и инлайн кнопку с ссылкой
        await message.reply('Вы в главном меню!') 
        await message.answer(txt_3, reply_markup=keyboard.btn_menu_start)
    else: # Если пользователь не найден, записываем его в БД и наводим на регистрацию
        await rq.set_user(message.from_user.id)
        await message.reply("Приветствую!")
        await message.answer('Выберите язык интерфейса',reply_markup=keyboard.btn_langMenu)

# Обработчик для команды /help и кнопки F.A.Q.
@rt.message(Command("help"))
@rt.message(F.text.contains('F.A.Q'))
async def cmd_help(message: types.Message):
    txt_1 = txt.text_1 # Текст с помощью
    await message.answer(txt_1)
# Обработчик для команды /ask 
@rt.message(Command("ask"))
async def cmd_ask(message: types.Message):
    txt_2 = txt.text_2 # Текст с адресом на Тех.поддержку
    await message.answer(txt_2)

# Обработчик для команды /profile и кнопки Профиль
@rt.message(Command("profile"))
@rt.message(F.text.contains('Профиль'))
async def send_profile(message: types.Message):
    user_id = message.from_user.id # Получаем ID пользователя
    user_name = message.from_user.full_name # Получаем Имя пользователя
    response = f"👤 Имя пользователя: {user_name}\n🔖 ID пользователя: {user_id}" # Готовим ответ
    await message.reply(response)

# Обработчик для кнопки Настройки 
@rt.message(F.text == '⚙️Настройки')
async def cmd_settings(message: types.Message):
    await message.answer('В этом разделе вы можете изменить настройки!',reply_markup=keyboard.btn_settings) # Подключаем инлайн кнопку с выбором параметров

# Обработчик для выбора инлайн кнопки языка
@rt.callback_query(F.data == 'Lang_RU')
@rt.callback_query(F.data == 'Lang_EU')
async def lang(callback: types.CallbackQuery):
    await callback.message.answer('Вы выбрали язык! Теперь пройдите регистрацию!',show_alert = True, reply_markup=keyboard.btn_reg) # Подключаем инлайн кнопку с регой

# Обработчик для регистрации
@rt.callback_query(F.data == 'regist')
async def send_reg(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Register.name) # Устанавливаем состояние для ввода имени
    await callback.message.answer('Введите ваше имя') # Делаем запрос имени

# Обработчик получения имени юзера
@rt.message(Register.name)
async def reg_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text) # Сохраняем имя в состоянии
    await state.set_state(Register.number) # Переход к состоянию ввода номера 
    await message.answer('Введите ваш номер телефона', reply_markup=keyboard.btn_number) # Запрос контакта

# Обработчик для получения контакта/номера от юзера
@rt.message(Register.number, F.contact)
async def reg_num(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number) # Сохраняем номер в состоянии
    data = await state.get_data() # Получаем сохраненные данные
    await message.answer(f'Ваше имя: {data["name"]}\nНомер: {data["number"]}\nОбновите бота командой /start', reply_markup=keyboard.kb) # Отправляем текст с готовыми данными
    await rq.set_name(data['name']) # Сохраняем имя в БД
    await rq.set_number(data['number']) # Сохраняем номер в БД
    await state.clear() # Очищаем






    

