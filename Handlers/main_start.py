from loader import dp, bot

from Filters import *
from States import *
from Database.users import *
from Database.attacks import *
from JsonParser.parser import *
from Modules.IPLookup.lookup import *
import Keyboards.main_kb as kb

from aiogram import Bot, types
from aiogram.dispatcher import FSMContext

import datetime


@dp.message_handler(IsWork(), IsPrivate(), commands=['start'])
async def process_start_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await addUser(user_id)

    await message.answer(f'🚀 <b>Welcome to KarmaAPI!</b>\n\n'
                         f'One of the leading DDoS tools with the best L4/L7 bypasses. Our bot is one of the best in terms of price and quality.\n\n'
                         f'🔽 <b>Use keyboard to navigate</b>', reply_markup=await kb.start_kb())


@dp.message_handler(IsWork(), IsPrivate(), state=UserStates.attackState)
async def process_start_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    await state.update_data(attackState=message.text)
    data = await state.get_data()
    user_input = data['attackState']

    args = user_input.split()

    if len(args) == 4:
        target = args[0]
        method = args[1]
        time = args[2]
        port = args[3]

        await startAttack(user_id, target, method, time, port, state)
        await state.finish()
    else:
        answ = (f'📝 <b>Not enough arguments to launch an attack.</b>\n'
                f"⤷ Usage: <code>[TARGET] [METHOD] [TIME] [PORT]</code>")
        await message.answer(answ, reply_markup=await kb.cancel_kb())


@dp.message_handler(IsWork(), IsPrivate(), content_types=types.ContentType.TEXT, text='🎯 Attacks')
async def handle_hello(message: types.Message):
    user_id = message.from_user.id
    await addUser(user_id)

    answ = (f'📝 <b>To launch the attack, enter the data:</b>\n'
            f"⤷ <code>[TARGET] [METHOD] [TIME] [PORT]</code>")
    await message.answer(answ, reply_markup=await kb.cancel_kb())

    await UserStates.attackState.set()


@dp.callback_query_handler(IsWork(), text="cancel", state='*')
async def scall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('✅ <b>Operation canceled successfully!</b>')
    await state.finish()


@dp.message_handler(IsWork(), IsPrivate(), content_types=types.ContentType.TEXT, text='👤 My Account')
async def handle_hello(message: types.Message):
    user_id = message.from_user.id
    await addUser(user_id)

    info = await getUserInfo(user_id)
    plan = info[2]
    expire = info[3]
    concs = info[4]
    maxtime = info[5]
    api = info[6]
    vip = info[7]

    if api == "True":
        api = '✅'
    else:
        api = '❌'

    if vip == "True":
        vip = '✅'
    else:
        vip = '❌'

    date_time = datetime.datetime.fromtimestamp(expire)
    now = datetime.datetime.now()
    delta = date_time - now
    days = delta.days

    if plan == "None":
        answ = (f'👤 <b>My Account</b>\n\n'
                f'· ID: <code>{user_id}</code>\n\n'
                f'❗ <b>You dont have an active plan!</b>')
    else:
        answ = (f'👤 <b>My Account</b>\n\n'
                f'· ID: <code>{user_id}</code>\n'
                f'· Plan: <b>{plan}</b>\n'
                f'· Expire: <b>{days}</b> days\n'
                f'· Concurrents: <b>{concs}</b>\n'
                f'· Maximum Time: <b>{maxtime}</b> sec.\n'
                f'· API Access: {api}\n'
                f'· VIP: {vip}\n\n'
                f'ℹ️ <b>You have an active plan.</b>')

    await message.answer(answ, reply_markup=await kb.links_kb())


@dp.message_handler(IsWork(), IsPrivate(), content_types=types.ContentType.TEXT, text='⚡ Plans')
async def handle_hello(message: types.Message):
    user_id = message.from_user.id
    await addUser(user_id)

    plans = ''

    answ = (f'🛡️ <b>Pricing plans:</b>\n\n'
            f'▸ <b>Basic</b>:\n'
            f'Concurrent: <code>1</code>\n'
            f'MaxTime: <code>300 seconds</code>\n'
            f'VIP: <code>❌</code>\n'
            f'API Access: <code>❌</code>\n'
            f'Cost: <code>15$/Month</code>\n\n'
            
            f'▸ <b>Standart</b>:\n'
            f'Concurrent: <code>2</code>\n'
            f'MaxTime: <code>600 seconds</code>\n'
            f'VIP: <code>❌</code>\n'
            f'API Access: <code>❌</code>\n'
            f'Cost: <code>35$/Month</code>\n\n'
            
            f'▸ <b>Premium</b>:\n'
            f'Concurrent: <code>3</code>\n'
            f'MaxTime: <code>1200 seconds</code>\n'
            f'VIP: <code>❌</code>\n'
            f'API Access: <code>✅</code>\n'
            f'Cost: <code>65$/Month</code>\n\n'
            
            f'▸ <b>Master</b>:\n'
            f'Concurrent: <code>4</code>\n'
            f'MaxTime: <code>2000 seconds</code>\n'
            f'VIP: <code>✅</code>\n'
            f'API Access: <code>✅</code>\n'
            f'Cost: <code>120$/Month</code>\n\n'
            f'➖➖➖➖➖➖➖➖➖➖\n'
            f'ℹ️ <b>For purchase — {Config().Support}</b>')

    for plan in Config().Plans:
        vip_smiley = '✅' if plan['VIP'] else '❌'
        api_smiley = '✅' if plan['API'] else '❌'

        plans += f'▸ <b>{plan["Name"]}</b>:\n'
        plans += f'Concurrent: <code>{plan["Concurrents"]}</code>\n'
        plans += f'MaxTime: <code>{plan["MaxTime"]} seconds</code>\n'
        plans += f'VIP: <code>{vip_smiley}</code>\n'
        plans += f'API Access: <code>{api_smiley}</code>\n'
        plans += f'Cost: <code>${plan["Cost"]}/Month</code>\n\n'

    answ1 = (f'🛡️ <b>Pricing plans:</b>\n\n'
             f'{plans}'
             f'➖➖➖➖➖➖➖➖➖➖\n'
             f'ℹ️ <b>For purchase — {Config().Support}</b>')

    await message.answer(answ1)


@dp.message_handler(IsWork(), IsPrivate(), content_types=types.ContentType.TEXT, text='📚 Methods')
async def handle_hello(message: types.Message):
    user_id = message.from_user.id
    await addUser(user_id)

    answ = (f'🔰 <b>Available methods:</b>\n\n'
            f'<b>📈 LAYER 7:</b>\n'
            f'~ <code>HTTP-FLOOD</code> – Method is useful against regular webservers/low protected targets.\n'
            f'~ <code>HTTP-STORM</code> – It sends a very stable stream of HTTP/2 requests per second and it can also bypass some JS challenges. <b>[VIP]</b>\n'
            f'~ <code>BROWSER</code> – Emulates a real user, which allows you to bypass Captcha or JS challenges.\n\n'
            f'<b>📉 LAYER 4:</b>\n'
            f'~ <code>UDP</code> - Sending a lot of UDP packets.\n'
            f'~ <code>TCP</code> - High PPS flood.\n'
            f'~ <code>OVH-TCP</code> – TCP flood to bypass OVH.\n'
            f'~ <code>SOCKET</code> – SOCKET flood.\n\n'
            f'➖➖➖➖➖➖➖➖➖➖\n'
            f'ℹ️ <b>More methods will be coming soon.</b>')

    await message.answer(answ)


@dp.message_handler(IsWork(), IsPrivate(), content_types=types.ContentType.TEXT, text='📦 Tools')
async def handle_hello(message: types.Message):
    user_id = message.from_user.id
    await addUser(user_id)

    answ = (f'🔽 <b>Select tool:</b>')
    await message.answer(answ, reply_markup=await kb.tools_kb())


@dp.callback_query_handler(IsWork(), text="lookup")
async def scall(call: types.CallbackQuery, state: FSMContext):

    answ = (f'📝 <b>Enter IP or domain...</b>')
    await call.message.answer(answ)
    await UserStates.lookupState.set()


@dp.message_handler(IsPrivate(), IsWork(), state=UserStates.lookupState)
async def handle_hello(message: types.Message, state: FSMContext):
    await state.update_data(lookupState=message.text)
    data = await state.get_data()
    user_input = data['lookupState']

    await message.answer('⌛')

    ipinfo = await iplookup(user_input)

    if ipinfo != False:
        answ = (f'🔍 <b>Information about {user_input}</b>\n\n'
                f'· IP: <code>{ipinfo[0]}</code>\n'
                    f'· Name: <code>{ipinfo[1]}</code>\n'
                    f'· Organization: <code>{ipinfo[2]}</code>\n'
                    f'· Provider: <code>{ipinfo[3]}</code>\n'
                    f'· Country: <code>{ipinfo[4]}</code>\n'
                    f'· City: <code>{ipinfo[5]}</code>\n\n'
                    f'<i>Checked by module IP Lookup</i> 🛡️')
    else:
        answ = (f'❗ <b>Could not find information about this resource.</b>')

    await message.answer(answ)
    await state.finish()

"""

Христе Боже распети и свети,
Српска земља кроз облаке лети.
Лети преко небеских висина,
Крила су јој Морава и Дрина.
 
Збогом први нерођени сине,
Збогом ружо, збогом рузмарине.
Збогом лето, јесени и зимо,
Одлазимо да се не вратимо.

На три свето и на три саставно,
Одлазимо на Косово равно.
Одлазимо на суђено место
Збогом мајко, сестро и невесто.
 
Збогом први нерођени сине,
Збогом ружо, збогом рузмарине.
Збогом лето, јесени и зимо.
Одлазимо да се не вратимо.

"""