### Файл с реализацией хендлеров ###

import requests
import sqlite3
import aiosqlite

from aiogram import types, Router, F, Bot
from aiogram.types import Message
from aiogram.filters.command import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from config_file import config # Импортируем файл для работы с .env
import keyb as keyboard # Импортируем файл с кнопками
import texts as txt # Импортируем файл с текстами
import data_base.req as rq # Подключаем файл с реализацией функций внесесения пользователей в БД
import data_base.que_reply as qr # Подключаем тогда, когда хотим затестить вопросно-ответные пары из БД
from middlewares import AccessMiddleware, BanUserMiddleware # Импорт MW
from filters import checkAdminFilter, adm # Импорт фильтра проверки на админа
from test import ai_text # Импорт обучалки


admin = config.admins
rt = Router() # Отделяем файл с хендлерами от остальных модулей
rt.message.middleware(AccessMiddleware()) # Подключение пропускного миддлвэйра к роутеру
rt.message.middleware(BanUserMiddleware()) # Подключение бан-миддлвэйра к роутеру

# Класс состояния регистрации пользователя по параметрам: Имя, Номер телефона
class Register(StatesGroup):
    name = State()
    number = State()

# Состояние для блокировки/разблокировки пользователя
class dialog(StatesGroup):
    ban = State()
    unban = State()

# Функция для получения ответа на заданный вопрос из бд(отключена от работы)
#async def get_answer(question):
    #async with aiosqlite.connect('vopros_otvet.db') as qr.conn: # Открываем асинхронное соединение с базой данных 'vopros_otvet.db'
        #async with qr.conn.execute("SELECT answer FROM menu WHERE question=?", (question,)) as cursor:  # Выполняем асинхронный SQL-запрос для извлечения ответа на заданный вопрос
            #result = await cursor.fetchone() # Извлекаем первую строку результата запроса
            #return result[0] if result else None  # Если результат существует, возвращаем ответ, иначе возвращаем None

# Обработчик для команды /start
@rt.message(CommandStart())
async def cmd_start(message: types.Message):
    con = sqlite3.connect('db.sqlite3') # Подключение к базе данных SQLite3
    cursor = con.cursor() # Создаем курсор для выполнения SQL запросов
    cursor.execute(f"SELECT tg_id FROM users WHERE tg_id = {message.from_user.id}")  # Запрос для проверки, существует ли пользователь в базе данных по его TG_ID
    user_id_massive = cursor.fetchall()
    txt_3 = txt.text_3 # Текст главного меню
    if user_id_massive: # Если пользователь найден, отправляем сообщение главного меню и инлайн кнопку с ссылкой
        await message.reply('Вы в главном меню!') 
        await message.answer(txt_3, reply_markup=keyboard.btn_menu_start)
    else: # Если пользователь не найден, записываем его в БД и наводим на регистрацию
        await message.reply("Приветствую!")
        await message.answer('Пройдите регистрацию в боте! ',reply_markup=keyboard.btn_reg)
    if message.from_user.id == admin and user_id_massive: # Проверка пользователя на админа
        await message.answer('Вы авторизованы как Администратор!',reply_markup=keyboard.kb_admin)

# Обработчик для кнопки "Админ Панель" + проверка на админа
@rt.message(checkAdminFilter(adm), F.text == '💼Админ Панель')
async def admin_commands(message: types.Message):
    await message.answer('Меню Администратора',reply_markup=keyboard.btn_admin)

# Обработчик для команды /help и кнопки F.A.Q.
@rt.message(Command("help"),StateFilter(None))
@rt.message(F.text.contains('F.A.Q'))
async def cmd_help(message: types.Message):
    txt_1 = txt.text_1 # Текст с помощью
    await message.answer(txt_1)

# Обработчик для команды /ask 
@rt.message(Command("ask"), StateFilter(None))
async def cmd_ask(message: types.Message):
    txt_2 = txt.text_2 # Текст с адресом на Тех.поддержку
    await message.answer(txt_2)

# Обработчик для команды /profile и кнопки Профиль
@rt.message(Command("profile"),StateFilter(None))
@rt.message(F.text.contains('Профиль'))
async def send_profile(message: types.Message):
    user_id = message.from_user.id # Получаем ID пользователя
    user_name = message.from_user.full_name # Получаем Имя пользователя
    response = f"👤 Имя пользователя: {user_name}\n🔖 ID пользователя: {user_id}" # Готовим ответ
    await message.reply(response)

# Обработчик для команды /order_cert из Быстрого меню
@rt.message(Command("order_cert"),StateFilter(None))
async def send_sert(message: types.Message):
    await message.answer("Заказать справку можно в личных сообщениях у <a href = 'https://t.me/hr_krasintegra'>HR Krasintegra</a>",parse_mode='HTML')

# Обработчик для команды /write_note из Быстрого меню
@rt.message(Command("write_note"),StateFilter(None))
async def link_docs(message: types.message):
    await message.answer('Ссылки на образцы документов: ')

# Обработчик для команды /hospital из Быстрого меню
@rt.message(Command("hospital"),StateFilter(None))
async def sick_leave(message: types.Message):
    await message.answer("<a href = 'https://t.me/hr_krasintegra'>HR Krasintegra</a>",parse_mode = 'HTML')

# Обработчик для команды /life_circum из Быстрого меню
@rt.message(Command('life_circum'),StateFilter(None))
async def send_life(message: types.Message):
    await message.answer('Перейдите по этой ссылке, чтобы узнать подробности: ')

# Обработчик для команды /my_vac из Быстрого меню
@rt.message(Command("my_vac"),StateFilter(None))
async def info_vac(message: types.Message):
    await message.answer('Выбери одну из опций:',reply_markup=keyboard.btn_my_vac)

# Обработчик для команды /my_term из Быстрого меню
@rt.message(Command("my_term"),StateFilter(None))
async def info_term(message: types.Message):
    await message.answer('Выбери одну из опций:',reply_markup=keyboard.btn_my_term)

# Обработчик для кнопки Настройки 
@rt.message(F.text == '⚙️Настройки')
async def cmd_settings(message: types.Message):
    await message.answer('В этом разделе вы можете изменить настройки!',reply_markup=keyboard.btn_settings) # Подключаем инлайн кнопку с выбором параметров

# Обработчик для регистрации
@rt.callback_query(F.data == 'regist')
async def send_reg(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Register.name) # Устанавливаем состояние для ввода имени
    await callback.message.answer('Введите ваше имя') # Делаем запрос имени

# Обработчик для инлайн кнопки "Заблокировать пользователя"
@rt.callback_query(checkAdminFilter(adm),F.data == 'ban_user')
async def black_list(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(dialog.ban) # Устанавливаем состояние для ввода ID
    await callback.message.answer('Введите ID пользователя')

# Обработчик для инлайн кнопки "Разблокировать пользователя"
@rt.callback_query(checkAdminFilter(adm), F.data == 'unban_user')
async def unban(callback: types. CallbackQuery, state: FSMContext):
    await state.set_state(dialog.unban) # Устанавливаем состояние для ввода ID
    await callback.message.answer('Введите ID Пользователя')

# Обработчик для инлайн кнопки "Статистика"
@rt.callback_query(checkAdminFilter(adm), F.data == 'statistic_users')
async def statistic(callback: types. CallbackQuery):
    con4 = sqlite3.connect('db.sqlite3') # Подключаемся к бд
    cursor4 = con4.cursor() # Создаем курсор 
    cursor4.execute('''SELECT tg_id, name, number FROM users''') # Делаем запрос по базе
    users_tg = cursor4.fetchall() # Создаем список
    sum_users = len(set(id[0] for id in users_tg)) # Делаем подсчет юзеров по списку 
    if users_tg: # Вывод данных из колонок
        message = '👥Информация о базе данных пользователей\n\n'
        for tg_id, name, number in users_tg:
            message += (f"👤ID Пользователя: {tg_id}\n"
                        f"📝ФИО Пользователя: {name}\n"
                        f"☎️Номер Пользователя: {number}"
                        f"\n〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\n")
        message += f"Всего пользователей в боте: {sum_users}"
    else:
        message = 'Нет данных о людях'
    await callback.message.answer(message) 

# Обработчик для состояния блокировки юзера
@rt.message(dialog.ban) 
async def banan(message: types.Message, state: FSMContext):
    await state.update_data(ban=message.text) # Сохраняем ID в состоянии 
    data_ban = await state.get_data() # Получаем сохраненные данные
    await message.answer('✅ Пользователь успешно заблокирован!')
    await rq.set_ban(data_ban['ban']) # Заносим ID в БД
    con2 = sqlite3.connect('db.sqlite3') # Подключение к БД
    cursor2 = con2.cursor() # Создаем курсор для запросов
    cursor2.execute(f'DELETE FROM allow_users WHERE allow_tg_id = ?', (data_ban['ban'],)) # Удаляем запись из вайтлиста
    con2.commit() # Сохраняем
    await state.clear() # Чистим состояние

# Обработчик для состояния разбана юзера
@rt.message(dialog.unban) 
async def unbanan(message: types.Message, state: FSMContext):
    await state.update_data(unban=message.text) # Сохраняем ID в состоянии 
    data_unban = await state.get_data()  # Получаем сохраненные данные
    await message.answer('✅ Пользователь успешно разблокирован!')
    con3 = sqlite3.connect('db.sqlite3') # Подключение к БД
    cursor3 = con3.cursor() # Создаем курсор для запросов
    cursor3.execute(f'INSERT INTO allow_users (allow_tg_id) VALUES (?)', (data_unban['unban'],)) # Добавляем запись в вайтлист
    cursor3.execute(f'DELETE FROM blocked WHERE block_tg_id = ?', (data_unban['unban'],)) # Удаляем запись из блеклиста
    con3.commit() # Сохраняем
    await state.clear() # Чистим состояние

# Обработчик получения имени юзера
@rt.message(Register.name, F.text)
async def reg_name(message: types.Message, state: FSMContext):
    if message.text.startswith('/'): # Условие проверки валидности данных
        await message.answer('Нельзя использовать команды, пока не пройдете регистрацию!')
        return
    await state.update_data(name=message.text) # Сохраняем имя в состоянии
    await state.set_state(Register.number) # Переход к состоянию ввода номера 
    await message.answer('Введите ваш номер телефона', reply_markup=keyboard.btn_number)

# Обработчик для получения данных от юзера и завершение состояния
@rt.message(Register.number, F.contact)
async def reg_num(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number) # Сохраняем номер в состоянии
    data = await state.get_data() # Получаем сохраненные данные
    await message.answer(f'Ваше имя: {data["name"]}\nНомер: {data["number"]}\nОбновите бота командой /start', reply_markup=keyboard.kb) # Отправляем текст с готовыми данными
    await rq.set_user(message.from_user.id, data['name'], data['number']) # Заносим данные в БД
    await state.clear() # Очищаем

# Обработчик для получения ответа на заданный вопрос(Отключен)
#@rt.message()
#async def handle_query(message: types.Message):
    #answer = await get_answer(message.text)
    #if answer:
        #await message.answer(answer)
    #else:
        #await message.answer('Не могу найти ответ на данный вопрос!')

# Обработчик для LLM
@rt.message(StateFilter(None))
async def message_handler(msg: Message, bot: Bot):
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'model': 'qwen2.5-7b-instruct-1m',
        'messages': [
            {
                'role': 'system',
                'content': ai_text,
            }, 
            {
                'role': 'user',
                'content': msg.text,
            },
        ],
        'temperature': 0.8,
        'max_tokens': -1,
        'stream': False,
    }

    response = requests.post(config.llm_url, headers=headers, json=json_data)
    data = response.json()
    text = data['choices'][0]['message']['content']

    await bot.send_message(msg.chat.id, text, parse_mode='Markdown')






    

