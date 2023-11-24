

from Initialization.init import *
from Handlers import dp
from JsonParser.parser import *
from Database.users import * 
from Utils.colors import *

import Filters

from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime
import asyncio, sys, logging, os

logging.basicConfig(level=logging.ERROR)

def handle_exception(exc_type, exc_value, exc_traceback):
    print(f'{c.lred}[Main]{c.reset} Error: {c.lred}[ {exc_value} ]{c.reset}')

sys.excepthook = handle_exception


async def on_startup(dp):
    Filters.setup(dp)

    asyncio.create_task(checkPlanLoop())

    print(f'[Main]{c.reset} Bot started{c.reset}')


async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()

    print(f'[Main]{c.reset} Stopped Every [ {Config().Version} ]{c.reset}')
    sys.exit(0)


if __name__ == "__main__":
    print(f'[Main]{c.reset} Starting Every [ {Config().Version} ]{c.reset}')
    initDB()
    print(f'[JSON] {c.reset}Correctly Loaded {loadedConfigs} {c.reset}configs')
    print(f'[Servers] {c.reset}Loaded {len(Servers().Servers)} {c.reset}servers')
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
