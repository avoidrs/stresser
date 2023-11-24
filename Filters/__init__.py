from aiogram import Dispatcher

from .filters import *

def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)
