### Файл с реализцией клавиатурных и инлайн кнопок ###

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Основная клавиатура с кнопками исполнения команд 
kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = '👤Профиль')], # Исполнение /profile
                                   [KeyboardButton(text = '⚙️Настройки')], # Самостоятельная кнопка с переводом на инлайн btn_settings
                                   [KeyboardButton(text = '❓F.A.Q')]], # Исполнение /help
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

# Кнопка с функцией "Поделиться контактом" на этапе регистрации
btn_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер',
                                                           request_contact=True, one_time_keyboard=True)]],
                                 resize_keyboard=True)

# Инлайн кнопка с ссылкой в главном меню после исполнения /start
btn_menu_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Подписаться на канал!', callback_data='menu_start', url='https://t.me/+md2DggzeBkc4MjM6')]])