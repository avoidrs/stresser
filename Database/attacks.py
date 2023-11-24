from loader import dp, bot

from JsonParser.parser import *
from Logging.send import *
from .users import *
import Keyboards.main_kb as kb
from Utils.colors import *

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import sqlite3
import asyncio
import re
import requests
import sys


def handle_exception(exc_type, exc_value, exc_traceback):
    print(f'{c.lred}[Main]{c.reset} Error: {c.lred}[ {exc_value} ]{c.reset}')

sys.excepthook = handle_exception

async def checkConcs(user_id):
    conn = sqlite3.connect('SQL/users.db')
    c = conn.cursor()

    c.execute("SELECT concs FROM users WHERE user_id=?", (user_id,))
    concs = c.fetchone()[0]

    conn.close()

    conn = sqlite3.connect('SQL/attacks.db')
    c = conn.cursor()

    c.execute(
        "SELECT COUNT(*) FROM attacks WHERE active = 1 AND user_id=?", (user_id,))
    count = c.fetchone()[0]

    if count >= concs:
        return False
    else:
        return True


async def checkActive():
    conn = sqlite3.connect('SQL/attacks.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM attacks WHERE active = 1")
    count = c.fetchone()[0]

    conn.close()

    if count >= Config().MaxSlots:
        return False
    else:
        return True


async def startAttack(user_id, target, method, time, port, state):
    for methods in Methods().Methods:
        if methods["Name"] == method:
            level = methods['Level']
            isVip = methods['VIP']

            info = await getUserInfo(user_id)

            if info[2] == 'None':
                answ = (f'❗ <b>An error occurred while launching the attack!</b>\n'
                        f"⤷ Error: <code>You do not have an active plan.</code>")
                await bot.send_message(user_id, answ)
                return
            
            if isVip == True:
                if info[7] == "False":
                    answ = (f'❗ <b>An error occurred while launching the attack!</b>\n'
                            f"⤷ Error: <code>This method requires VIP access.</code>")
                    await bot.send_message(user_id, answ)
                    return

            if level == 'L7':
                if not re.match(r'^https?://', target):
                    answ = (f'❗ <b>An error occurred while launching the attack!</b>\n'
                            f"⤷ Error: <code>Target is not a valid URL</code>")
                    await bot.send_message(user_id, answ)
                    return

            if level == 'L4':
                if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
                    answ = (f'❗ <b>An error occurred while launching the attack!</b>\n'
                            f"⤷ Error: <code>Target is not a valid IP address.</code>")
                    await bot.send_message(user_id, answ)
                    return

            if not time.isdigit():
                answ = (f'❗ <b>An error occurred while launching the attack!</b>\n'
                        f"⤷ Error: <code>Time must be an integer.</code>")
                await bot.send_message(user_id, answ)
                return

            if not port.isdigit():
                answ = (f'❗ <b>An error occurred while launching the attack!</b>\n'
                        f"⤷ Error: <code>Port must be an integer.</code>")
                await bot.send_message(user_id, answ)
                return

            if int(port) <= 0 or int(port) > 65535:
                answ = (f'❗ <b>An error occurred while launching the attack!</b>\n'
                        f"⤷ Error: <code>Port must be between 0 and 65535.</code>")
                await bot.send_message(user_id, answ)
                return

            if int(time) < 30:
                answ = (f'❗ <b>An error occurred while launching the attack!</b>\n'
                        f"⤷ Error: <code>Minimum attack time - 30 seconds.</code>")
                await bot.send_message(user_id, answ)
                return

            if re.search(r'\.onion$', target):
                answ = (f'❗ <b>An error occurred while launching the attack!</b>\n'
                        f"⤷ Error: <code>Onion sites are temporarily unattackable.</code>")
                await bot.send_message(user_id, answ)
                return

            if not await checkActive():
                answ = (f'❗ <b>An error occurred while launching the attack!</b>\n'
                        f"⤷ Error: <code>All slots are full.</code>")
                await bot.send_message(user_id, answ)
                return

            if not await checkConcs(user_id):
                answ = (f'❗ <b>An error occurred while launching the attack!</b>\n'
                        f"⤷ Error: <code>All concurrents are full.</code>")
                await bot.send_message(user_id, answ)
                return

            if int(time) > info[5]:
                answ = (f'❗ <b>An error occurred while launching the attack!</b>\n'
                        f"⤷ Error: <code>All concurrents are full.</code>")
                await bot.send_message(user_id, answ)
                return

            """
            if any(item in target for item in Config().Blacklists):
                answ = (f'❗ <b>An error occurred while launching the attack!</b>\n'
                        f"⤷ Error: <code>This target is blacklisted.</code>")
                await bot.send_message(user_id, answ)
                return
            """

            for item in ['.gov', 'gov.', '.edu', 'edu.']:
                if item in target:
                    if item in ['.gov', 'gov.']:
                        message = (f'⚠️ <b>WARNING:</b> Launched attack on GOV website\n'
                                   f'<a href="tg://user?id={user_id}">User</a> has just launched an attack on a <a href="{target}">government website</a>.\n\n'
                                   f'🔍 <b>User information:</b>\n'
                                   f'├ ID: <code>{user_id}</code>\n'
                                   f'├ Plan: <code>{info[2]}</code>\n'
                                   f'├ Concurrents: <code>{info[4]}</code>\n'
                                   f'├ MaxTime: <code>{info[5]}</code>\n'
                                   f'└ VIP: <code>{info[7]}</code>\n\n'
                                   f'· Target: <b>{target}</b>\n'
                                   f'· Method: <b>{method}</b>\n'
                                   f'· Time: <b>{time}</b> sec.\n\n'
                                   f'ℹ️ Attacking government structures is prohibited in TOS.')
                    else:
                        message = (f'⚠️ <b>WARNING:</b> Launched attack on EDU website\n'
                                   f'<a href="tg://user?id={user_id}">User</a> has just launched an attack on a <a href="{target}">education website</a>.\n\n'
                                   f'🔍 <b>User information:</b>\n'
                                   f'├ ID: <code>{user_id}</code>\n'
                                   f'├ Plan: <code>{info[2]}</code>\n'
                                   f'├ Concurrents: <code>{info[4]}</code>\n'
                                   f'├ MaxTime: <code>{info[5]}</code>\n'
                                   f'└ VIP: <code>{info[7]}</code>\n\n'
                                   f'· Target: <b>{target}</b>\n'
                                   f'· Method: <b>{method}</b>\n'
                                   f'· Time: <b>{time}</b> sec.\n\n'
                                   f'ℹ️ Attacking government structures is prohibited in TOS.')
                    await sendAdmins(message)

            for url in methods["URL"]:
                print(
                    f"{url.format(target=target, time=time, method=method, port=port)}")
                r = requests.get(url.format(target=target, time=time, method=method, port=port))

            # data = r.json()
            # status = data['status']
            status = True

            if status == False:
                answ = (f'❗ <b>An error occurred while launching the attack, please try again later.</b>\n'
                        f"⤷ Error: <code>here error</code>")
                # data['message']
                await bot.send_message(user_id, answ)
                return

            if level == 'L7':
                markup = InlineKeyboardMarkup(row_width=1)
                checkhost = InlineKeyboardButton(
                    '🔥 CHECKHOST ›', url=f'https://check-host.net/check-http?host={target}')
                markup.add(checkhost)

                answ = (f'⚡ <b>Attack started!</b>\n\n'
                        f'· Target: <b>{target}</b>\n'
                        f'· Method: <b>{method}</b>\n'
                        f'· Time: <b>{time}</b> sec.\n'
                        f'· Level: <b>LAYER-7</b>\n\n'
                        f'🔥 Check Server Status › <b><a href="https://check-host.net/check-http?host={target}">CHECK-HOST</a></b>')

                await bot.send_message(user_id, '🚀')
                await bot.send_message(user_id, answ, reply_markup=markup)

            else:
                markup = InlineKeyboardMarkup(row_width=1)
                checkhost = InlineKeyboardButton(
                    '🔥 CHECKHOST ›', url=f'https://check-host.net/check-ping?host={target}:{port}')
                markup.add(checkhost)

                answ = (f'🎯 <b>Attack launched!</b>\n\n'
                        f'· Target: <b>{target}:{port}</b>\n'
                        f'· Method: <b>{method}</b>\n'
                        f'· Time: <b>{time}</b> sec.\n'
                        f'· Level: <b>LAYER-4</b>\n\n'
                        f'🔥 Check server status › <b><a href="https://check-host.net/check-ping?host={target}:{port}">CHECK-HOST</a></b>')

                await bot.send_message(user_id, '⛈️')
                await bot.send_message(user_id, answ, reply_markup=markup)
            
            await state.finish()

            await asyncio.sleep(int(time))

            answ = (f'⌛ <b>Attack completed!</b>\n\n'
                    f'· Target: <b>{target}</b>\n'
                    f'· Method: <b>{method}</b>\n'
                    f'· Time: <b>{time}</b> sec.')

            await bot.send_message(user_id, answ)
            return
    else:
        answ = (f'❗ <b>An error occurred while launching the attack,.</b>\n'
                f"⤷ Error: <code>Unknown method.</code>")
        await bot.send_message(user_id, answ)
        return


async def checkRunning():
    conn = sqlite3.connect('SQL/attacks.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM attacks WHERE active = 1")
    count = c.fetchone()[0]

    c.execute("SELECT target, time, method FROM attacks WHERE active = 1")
    results = c.fetchall()

    if len(results) == 0:
        return f'📉 <b>There are currently no active attacks.</b>'
    else:
        message = ''
        for i, row in enumerate(results):
            target, time, method = row
            message += f"#{i+1} ▸ <code>{target} | {time} | {method}</code>\n"

        return (f'🚀 <b>Now running</b> {count} <b>attacks</b>:\n\n'
                f'🔽   <code>#NUM</code>  ▸  <code>TARGET</code>  |  <code>TIME</code>  |  <code>METHOD</code>   🔽\n'
                f'{message}')
    

async def stopAll():
    conn = sqlite3.connect('SQL/attacks.db')
    c = conn.cursor()

    c.execute("SELECT * FROM attacks WHERE active=1")
    rows = c.fetchall()

    for row in rows:
        c.execute("UPDATE attacks SET active=0 WHERE id=?", (row[0],))

    conn.commit()
    conn.close()



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