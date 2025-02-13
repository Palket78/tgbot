from aiogram.types import Message
from aiogram.filters import BaseFilter

from config_file import config

adm = config.admins

class checkAdminFilter(BaseFilter):
    def __init__(self, adm) -> None:
        super().__init__()
        self.admin_ids = adm

    async def __call__(self, message: Message) -> None:
       return message.from_user.id == self.admin_ids