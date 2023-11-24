from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

async def admin_kb():
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    addPlan = KeyboardButton('📈 Issue plan')
    addMassDays = KeyboardButton('👥 Add all days')
    searchUser = KeyboardButton('🔍 Search user')
    broadcast = KeyboardButton('📢 Broadcast')
    ongoing = KeyboardButton('🚀 Ongoing')
    debug = KeyboardButton('📟 Debug information')
    removePlan = KeyboardButton('🚷 Remove plan')
    stopAttacks = KeyboardButton('⛔ Stop attacks')

    markup.add(addPlan, addMassDays, searchUser)
    markup.add(broadcast, ongoing, debug)
    markup.add(removePlan, stopAttacks)

    return markup


async def send_bc_kb():
    markup = InlineKeyboardMarkup(row_width=2)

    yes_send = InlineKeyboardButton('✅ Send', callback_data='yes_send')
    no_send = InlineKeyboardButton('❌ Cancel', callback_data='no_send')

    markup.add(yes_send, no_send)

    return markup


async def cancel_kb():
    markup = InlineKeyboardMarkup(row_width=2)

    cancel = InlineKeyboardButton('❌ Cancel', callback_data='cancel')

    markup.add(cancel)

    return markup