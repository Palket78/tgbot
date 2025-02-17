### Конфиг файл для работы с .env

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

# Класс определения переменных в .env файле
class Tg_Config(BaseSettings):
    bot_token: SecretStr # Определяем переменную bot_token как SecretStr для хранения конф.данных
    admins: int # Определяем переменную admins как integer
    llm_url: str # Определяем переменную llm_url как String
    sql_url: str # Да тут тоже самое
    #  Конфигурируем загрузку переменных окружения из файла .env с кодировкой utf-8
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8',env_prefix='',env_nested_delimiter='__')

config = Tg_Config() # Создаем экземпляр класса