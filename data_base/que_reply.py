### ФАЙЛ ДЛЯ РАБОТЫ С ВОПРОСНО-ОТВЕТНЫМИ ПАРАМИ ###

import aiosqlite
import logging

import texts as txt1

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Глобальные переменные для соединения с БД
conn = None
cur = None

async def sql_start():
    global conn, cur
    conn = await aiosqlite.connect('vopros_otvet.db')
    cur = await conn.cursor()
    logging.info('Data base connected!')

    # Создаем таблицу для хранения вопросов и ответов
    await cur.execute('CREATE TABLE IF NOT EXISTS menu(id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT UNIQUE, answer TEXT)')

    # Добавляем заранее подготовленные вопросы и ответы
    qa_pairs = txt1.text_4

    # Добавляем пары вопросов и ответов в базу данных
    for question, answer in qa_pairs.items():
        try:
            await cur.execute('INSERT INTO menu (question, answer) VALUES (?, ?)', (question, answer))
        except aiosqlite.IntegrityError:
            # Если вопрос уже существует, игнорируем ошибку
            logging.warning(f"Вопрос '{question}' уже существует в базе данных.")

    await conn.commit()

async def sql_add_command(question, answer):
    await cur.execute('INSERT INTO menu (question, answer) VALUES (?, ?)', (question, answer))
    await conn.commit()

async def get_all_questions():
    async with conn.execute("SELECT question FROM menu") as cursor:
        questions = await cursor.fetchall()
        return [q[0] for q in questions]

async def list_questions():
    async with conn.execute("SELECT question FROM menu") as cursor:
        return await cursor.fetchall()
    
async def close_connection():
    if conn:
        await conn.close()
        logging.info('Connection to database closed.')


 