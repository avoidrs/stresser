from JsonParser.parser import *

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


async def start_kb():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    attack = KeyboardButton('🎯 Attacks')
    #modules = KeyboardButton('📦 Tools')
    methods = KeyboardButton('📚 Methods')
    plans = KeyboardButton('⚡ Plans')
    account = KeyboardButton('👤 My Account')

    markup.add(attack, methods)
    markup.add(plans)
    markup.add(account)

    return markup


async def cancel_kb():
    markup = InlineKeyboardMarkup(row_width=2)

    cancel = InlineKeyboardButton('❌ Cancel', callback_data='cancel')

    markup.add(cancel)

    return markup


async def tools_kb():
    markup = InlineKeyboardMarkup(row_width=2)

    iplookup = InlineKeyboardButton('🔍 IP Lookup', callback_data='lookup')

    markup.add(iplookup)

    return markup


async def links_kb():
    markup = InlineKeyboardMarkup(row_width=2)

    news = InlineKeyboardButton('News →', url=f'{Config().News}')
    power = InlineKeyboardButton('Powerproof →', url=f'{Config().Power}')
    support = InlineKeyboardButton('Support →', url=f'{Config().Support}')

    markup.add(news)
    markup.add(power)
    markup.add(support)

    return markup