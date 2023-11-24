from loader import dp, bot

import Utils.colors as col

import sqlite3
import datetime
import time
import asyncio
import sys

def handle_exception(exc_type, exc_value, exc_traceback):
    print(f'{col.c.lred}[Main]{col.c.reset} Error: {col.c.lred}[ {exc_value} ]{col.c.reset}')

sys.excepthook = handle_exception

async def addUser(user_id):
    conn = sqlite3.connect('SQL/users.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    data = c.fetchone()

    if data:
        pass
    else:
        c.execute(f"INSERT INTO users (user_id) VALUES ({user_id})")
        conn.commit()
        print(f'{col.c.lblue}[SQL] {col.c.reset}Registered user {col.c.lblue}{user_id}{col.c.reset}')

    conn.close()


async def getUserInfo(user_id):
    conn = sqlite3.connect('SQL/users.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    data = c.fetchone()

    conn.close()

    return data


async def addPlan(user_id, plan, days, concs, maxtime, api, vip, key):
    conn = sqlite3.connect('SQL/users.db')
    c = conn.cursor()

    today = datetime.datetime.today()
    date = today + datetime.timedelta(days=int(days)+1)
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    timestamp = date.timestamp()

    c.execute("UPDATE users SET expire=? WHERE user_id=?", (timestamp, user_id,))
    conn.commit()

    c.execute("UPDATE users SET plan=? WHERE user_id=?", (plan, user_id,))
    conn.commit()

    c.execute("UPDATE users SET concs=? WHERE user_id=?", (concs, user_id,))
    conn.commit()

    c.execute("UPDATE users SET maxtime=? WHERE user_id=?", (maxtime, user_id,))
    conn.commit()

    c.execute("UPDATE users SET api=? WHERE user_id=?", (api, user_id,))
    conn.commit()

    c.execute("UPDATE users SET vip=? WHERE user_id=?", (vip, user_id,))
    conn.commit()

    c.execute("SELECT id FROM users WHERE user_id=?", (user_id,))
    id = c.fetchone()[0]

    conn.close()


    conn = sqlite3.connect('SQL/api.db')
    c = conn.cursor()

    c.execute("SELECT * FROM api WHERE id=?", (id,))
    data = c.fetchone()

    if data:
        c.execute("UPDATE api SET active=? WHERE id=?", (api, id,))
        conn.commit()

        c.execute("UPDATE api SET key=? WHERE id=?", (key, id,))
        conn.commit()

        c.execute("UPDATE api SET expire=? WHERE id=?", (timestamp, id,))
        conn.commit()
    else:
        c.execute("INSERT INTO api (id, key, expire, active) VALUES (?, ?, ?, ?)", (id, key, timestamp, api,))
        conn.commit()

    conn.close()

    answ = (f'🚀 Added <b>{days}</b> (<code>{timestamp}</code>) days for user <b>{user_id}</b>')
    return answ


async def addMassDays(days):
    conn = sqlite3.connect('SQL/users.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE plan != 'None'")
    users = c.fetchall()

    for user in users:
        expire_timestamp = user[3]
        if expire_timestamp:
            expire_date = datetime.datetime.fromtimestamp(expire_timestamp)
            expire_date += datetime.timedelta(days=int(days))
            expire_timestamp = int(expire_date.timestamp())

            c.execute("UPDATE users SET expire = ? WHERE id = ?", (expire_timestamp, user[0]))
            conn.commit()
            
    conn.close()


async def send_messages(text):
    conn = sqlite3.connect('SQL/users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT user_id FROM users')
    user_ids = cursor.fetchall()
    
    conn.close()

    for user_id in user_ids:
        try:
            await bot.send_message(user_id[0], text)
        except:
            pass


async def allDebug():
    conn = sqlite3.connect('SQL/users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT user_id FROM users')
    totalUsers = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM users WHERE plan <> 'None';")
    paidUsers = cursor.fetchone()[0]

    conn.close()


    conn = sqlite3.connect('SQL/attacks.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM attacks WHERE active = 1")
    nowRunning = cursor.fetchone()[0]

    cursor.execute('SELECT user_id FROM attacks')
    totalAttacks = cursor.fetchall()

    conn.close()
    return [len(totalUsers), len(totalAttacks), nowRunning, paidUsers]


async def checkPlanLoop():
    conn = sqlite3.connect('SQL/users.db')
    c = conn.cursor()

    while True:
        c.execute("SELECT user_id FROM users WHERE expire < ?", (time.time(),))
        expired_users = c.fetchall()

        for user_id in expired_users:
            c.execute("UPDATE users SET plan = 'None' WHERE user_id = ?", (user_id[0],))
            conn.commit()

        await asyncio.sleep(3)

    conn.close()


async def removePlan(user_id):
    conn = sqlite3.connect('SQL/users.db')
    c = conn.cursor()

    c.execute("UPDATE users SET plan = 'None' WHERE user_id = ?", (user_id,))
    conn.commit()

    c.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
    id = c.fetchone()[0]

    conn.close()


    conn = sqlite3.connect('SQL/api.db')
    c = conn.cursor()

    c.execute("SELECT * FROM api WHERE id = ?", (id,))
    data = c.fetchone()

    if data:
        c.execute("UPDATE api SET active = 'False' WHERE id = ?", (id,))
        conn.commit()

    conn.close()