from loader import dp, bot

from States import *
from Filters import *
from Database.users import *
from Database.attacks import *
from JsonParser.parser import *
import Keyboards.admin_kb as kb
from Utils.colors import *

from aiogram import Bot, types
from aiogram.dispatcher import FSMContext

import random
import string
import asyncio

@dp.message_handler(IsAdmin(), commands=['admin'])
async def process_start_command(message: types.Message):
    await message.answer(f'📟 <b>Welcome to Admin Panel!</b>\n\n'
                         f'Here you can manage users, bot and more..\n\n'
                         f'🔽 <b>Use keyboard to navigate</b>', reply_markup=await kb.admin_kb())


@dp.callback_query_handler(IsWork(), text="cancel", state='*')
async def scall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('✅ <b>Operation canceled successfully!</b>')
    await state.finish()



@dp.message_handler(IsAdmin(), IsPrivate(), content_types=types.ContentType.TEXT, text='📈 Issue plan')
async def handle_hello(message: types.Message):
    user_id = message.from_user.id

    answ = (f'📈 <b>Enter the data to issue the plan:</b>\n'
            f"⤷ <code>[ID] [PLAN] [DAYS]</code>")
    await message.answer(answ, reply_markup=await kb.cancel_kb())

    await AdminStates.addPlanState.set()


@dp.message_handler(IsAdmin(), state=AdminStates.addPlanState)
async def process_start_command(message: types.Message, state: FSMContext):
    await state.update_data(addPlanState=message.text)
    data = await state.get_data()
    user_input = data['addPlanState']

    args = user_input.split()
    if len(args) == 3:
        user_id = args[0]
        plans = args[1]
        days = args[2]

        found_plan = False
        for plan in Config().Plans:
            if plan['Name'] == plans:
                found_plan = True
                concs = plan['Concurrents']
                maxtime = plan['MaxTime']
                api = plan['API']
                vip = plan['VIP']
                key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
            
        if found_plan:
            await message.answer(await addPlan(user_id, plans, days, concs, maxtime, str(api), str(vip), key))
            await state.finish()
        else:
            answ = (f'❗ <b>Failed to issue plan to user.</b>\n'
                    f"⤷ Error: <code>Plan not found.</code>")
            await message.answer(answ)
            await state.finish()
    else:
        answ = (f'📝 <b>Not enough arguments to add plan.</b>\n'
                f"⤷ Usage: <code>[ID] [PLAN] [DAYS]</code>")
        await message.answer(answ, reply_markup=await kb.cancel_kb())



@dp.message_handler(IsAdmin(), IsPrivate(), content_types=types.ContentType.TEXT, text='👥 Add all days')
async def handle_hello(message: types.Message):
    user_id = message.from_user.id

    answ = (f'📈 <b>Enter the data to add days:</b>\n'
            f"⤷ <code>[DAYS]</code>")
    await message.answer(answ, reply_markup=await kb.cancel_kb())

    await AdminStates.addMassDaysState.set()


@dp.message_handler(IsAdmin(), state=AdminStates.addMassDaysState)
async def process_start_command(message: types.Message, state: FSMContext):
    await state.update_data(addMassDaysState=message.text)
    data = await state.get_data()
    user_input = data['addMassDaysState']

    args = user_input.split()
    if len(args) == 1:
        days = args[0]
        await addMassDays(days)
        answ = (f'🚀 Added to all users with plans <b>{days} days</b> to the subscription.')
        await message.answer(answ)
        await state.finish()
    else:
        answ = (f'📝 <b>Not enough arguments to add days.</b>\n'
                f"⤷ Usage: <code>[DAYS]</code>")
        await message.answer(answ, reply_markup=await kb.cancel_kb())



@dp.message_handler(IsAdmin(), IsPrivate(), content_types=types.ContentType.TEXT, text='🔍 Search user')
async def handle_hello(message: types.Message):
    user_id = message.from_user.id

    answ = (f'📈 <b>Enter the data to seach user:</b>\n'
            f"⤷ <code>[ID]</code>")
    await message.answer(answ, reply_markup=await kb.cancel_kb())

    await AdminStates.searchUserState.set()


@dp.message_handler(IsAdmin(), state=AdminStates.searchUserState)
async def process_start_command(message: types.Message, state: FSMContext):
    await state.update_data(searchUserState=message.text)
    data = await state.get_data()
    user_input = data['searchUserState']

    args = user_input.split()
    if len(args) == 1:
        user_id = args[0]

        try:
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
                answ = (f'👤 <b>{user_id} Account</b>\n\n'
                        f'· ID: <code>{user_id}</code>\n\n'
                        f'❗ <b>User dont have an active plan!</b>')
            else:
                answ = (f'👤 <b>{user_id} Account</b>\n\n'
                        f'· ID: <code>{user_id}</code>\n'
                        f'· Plan: <b>{plan}</b>\n'
                        f'· Expire: <b>{days}</b> days\n'
                        f'· Concurrents: <b>{concs}</b>\n'
                        f'· Maximum Time: <b>{maxtime}</b> sec.\n'
                        f'· API Access: {api}\n'
                        f'· VIP: {vip}\n\n'
                        f'ℹ️ <b>User have an active plan.</b>')
            await message.answer(answ)
            await state.finish()
        except:
            answ = (f'❗ <b>Failed to search user.</b>\n'
                    f"⤷ Error: <code>User not found.</code>")
            await message.answer(answ)
            await state.finish()
    else:
        answ = (f'📝 <b>Not enough arguments to search user.</b>\n'
                f"⤷ Usage: <code>[ID]</code>")
        await message.answer(answ, reply_markup=await kb.cancel_kb())


    
@dp.message_handler(IsAdmin(), IsPrivate(), content_types=types.ContentType.TEXT, text='📢 Broadcast')
async def handle_hello(message: types.Message):
    user_id = message.from_user.id

    answ = (f'📈 <b>Enter the broadcast message...</b>')
    await message.answer(answ, reply_markup=await kb.cancel_kb())

    await AdminStates.bcState.set()


@dp.message_handler(IsAdmin(), state=AdminStates.bcState)
async def process_scall(message: types.Message, state: FSMContext):
    await state.update_data(bcState=message.text)
    data = await state.get_data()
    user_input = data['bcState']

    answ = (f'📢 <b>Broadcast</b>\n'
            f'➖➖➖➖➖➖➖➖➖➖\n'
            f'{user_input}\n'
            f'➖➖➖➖➖➖➖➖➖➖\n'
            f'⚠️ Are you sure you want to send a broadcast?')
    
    await message.answer(answ, reply_markup=await kb.send_bc_kb())


@dp.callback_query_handler(IsAdmin(), text=["no_send", "yes_send"], state=AdminStates.bcState)
async def scall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data == "no_send":
        await state.finish()
        await call.message.answer(f'✅ <b>Canceled..</b>')

    else:
        await call.message.answer(f'📢 <b>Broadcast Sent successfully!</b>')
        async with state.proxy() as data:
            user_input = data['bcState']
        asyncio.create_task(send_messages(user_input))
        await state.finish()



@dp.message_handler(IsAdmin(), IsPrivate(), content_types=types.ContentType.TEXT, text='🚀 Ongoing')
async def handle_hello(message: types.Message):
    user_id = message.from_user.id

    await message.answer(await checkRunning())



@dp.message_handler(IsAdmin(), IsPrivate(), content_types=types.ContentType.TEXT, text='📟 Debug information')
async def handle_hello(message: types.Message):
    user_id = message.from_user.id

    info = await allDebug()

    answ = (f'📟 <b>Full debug information:</b>\n\n'
            f'· Total users: <code>{info[0]}</code>\n'
            f'· Total attacks: <code>{info[1]}</code>\n'
            f'· Ongoing count: <code>{info[2]}</code>\n'
            f'· Paid Users: <code>{info[3]}</code>')

    await message.answer(answ)



@dp.message_handler(IsAdmin(), IsPrivate(), content_types=types.ContentType.TEXT, text='🚷 Remove plan')
async def handle_hello(message: types.Message):
    user_id = message.from_user.id

    answ = (f'📈 <b>Enter the data to remove the plan:</b>\n'
            f"⤷ <code>[ID]</code>")
    await message.answer(answ, reply_markup=await kb.cancel_kb())

    await AdminStates.removePlanState.set()


@dp.message_handler(IsAdmin(), state=AdminStates.removePlanState)
async def process_start_command(message: types.Message, state: FSMContext):
    await state.update_data(removePlanState=message.text)
    data = await state.get_data()
    user_input = data['removePlanState']

    args = user_input.split()
    if len(args) == 1:
        user_id = args[0]
            
        try:
            await removePlan(user_id)
            answ = (f'📈 Plan for user <b>{user_id}</b> successfully removed!')
            await message.answer(answ)
            await state.finish()
        except:
            answ = (f'❗ <b>Failed to remove plan to user.</b>\n'
                    f"⤷ Error: <code>User not found.</code>")
            await message.answer(answ)
            await state.finish()
    else:
        answ = (f'📝 <b>Not enough arguments to add plan.</b>\n'
                f"⤷ Usage: <code>[ID]</code>")
        await message.answer(answ, reply_markup=await kb.cancel_kb())


@dp.message_handler(IsAdmin(), IsPrivate(), content_types=types.ContentType.TEXT, text='⛔ Stop attacks')
async def handle_hello(message: types.Message):
    user_id = message.from_user.id

    await stopAll()
    answ = (f'📈 <b>All attacks stopped.</b> (But in database only)')
    await message.answer(answ)