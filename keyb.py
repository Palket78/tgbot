### Файл с реализцией клавиатурных и инлайн кнопок ###

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import BotCommand
from aiogram import Bot

# Основная клавиатура с кнопками исполнения команд 
kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = '👤Профиль')], # Исполнение /profile
                                   [KeyboardButton(text = '⚙️Настройки')], # Самостоятельная кнопка с переводом на инлайн btn_settings
                                   [KeyboardButton(text = '❓F.A.Q')]], # Исполнение /help
                        resize_keyboard=True)

kb_admin = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = '👤Профиль')], # Исполнение /profile
                                   [KeyboardButton(text = '⚙️Настройки')], # Самостоятельная кнопка с переводом на инлайн btn_settings
                                   [KeyboardButton(text = '❓F.A.Q')],
                                   [KeyboardButton(text = '💼Админ Панель')]], 
                        resize_keyboard=True)

# Кнопка с функцией "Поделиться контактом" на этапе регистрации
btn_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер',
                                                           request_contact=True, one_time_keyboard=True)]],
                                 resize_keyboard=True)

# Инлайн кнопка с выбором параметров (будет дополняться)
btn_settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = '🇺🇳Язык интерфейса', callback_data='Lang_Int')]])

# Инлайн кнопки на этапе /start без идентификации с выбором языка(без локализации)
btn_langMenu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = '🇷🇺Русский', callback_data ='Lang_RU')],
    [InlineKeyboardButton(text = '🇺🇸English', callback_data = 'Lang_EU')]])

# Инлайн кнопка регистрация 
btn_reg = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Регистрация', callback_data = 'regist')]])

# Инлайн кнопка с ссылкой в главном меню после исполнения /start
btn_menu_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Подписаться на канал!', callback_data='menu_start', url='https://t.me/+md2DggzeBkc4MjM6')]])

btn_my_vac = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Узнать остаток', callback_data='find_rest')],
    [InlineKeyboardButton(text = 'Написать заявление на отпуск', callback_data='write_vac')],
    [InlineKeyboardButton(text = 'Перенести',callback_data='ret_m')],
    [InlineKeyboardButton(text = 'Табель отпусков на текущий год',callback_data='time_sheet')]])

btn_my_term = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Чек-лист', callback_data='check_list')],
    [InlineKeyboardButton(text = 'Штатное расписание',callback_data='staff',url = '')]])

btn_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Заблокировать пользователя',callback_data='ban_user')],
    [InlineKeyboardButton(text = 'Разблокировать пользователя',callback_data = 'unban_user')],
    [InlineKeyboardButton(text = 'Статистика',callback_data='statistic_users')]
])

# Фунция создания быстрого меню команд 
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command="/start", description="Перезапуск бота"),
        BotCommand(command="/profile", description="Мой аккаунт"),
        BotCommand(command="/help", description="Основная Информация"),
        BotCommand(command="/ask", description="Техническая Поддержка"),
        BotCommand(command="/order_cert",description="Заказать справку"),
        BotCommand(command="/write_note",description="Написать заявление"),
        BotCommand(command="/hospital",description="Мой больничный"),
        BotCommand(command="/life_circum",description="Жизненные обстоятельства"),
        BotCommand(command="/my_vac", description = "Мой отпуск"),
        BotCommand(command ="/my_term",description = "Мой испытательный срок")
        ]     
    await bot.set_my_commands(main_menu_commands)

        
