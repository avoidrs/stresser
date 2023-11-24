from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import bot

from JsonParser.parser import *


# Проверка на написания сообщения в ЛС бота
class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


# Проверка на админа
class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        if message.from_user.id in Config().Admins:
            return True
        else:
            return False
        

# Проверка на тех работы
class IsWork(BoundFilter):
    async def check(self, message: types.Message):
        if Config().Maintenance and message.from_user.id not in Config().Admins:

            answ = (f'🚧 <b>Maintenance Works</b>\n\n'
                    f"The bot is undergoing planned technical work. We update the bot, fix bugs and add a lot of new things. Don't worry, we'll be back soon!\n\n"
                    f'Read news - {Config().News}')

            await bot.send_message(message.from_user.id, answ)
            return False
        return True