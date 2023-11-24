from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from JsonParser.parser import *


bot = Bot(token=Config().Token, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
dp = Dispatcher(bot, storage=MemoryStorage())