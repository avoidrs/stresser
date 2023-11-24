from Utils.colors import *

import sqlite3
import os, sys


def initDB():
    loaded = 0
    try:
        conn = sqlite3.connect('SQL/users.db')
        cur = conn.cursor()

        cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            plan TEXT DEFAULT None,
            expire INTEGER DEFAULT 0,
            concs INTEGER DEFAULT 1,
            maxtime INTEGER DEFAULT 0,
            api TEXT DEFAULT "False",
            vip TEXT DEFAULT "False" 
        )''')

        conn.commit()
        conn.close()

        loaded += 1
    except Exception as e:
        print(f'{c.lred}[SQL] {c.reset}Database error: {c.lred} [ users.db - {e}]{c.reset}')

    try:
        conn = sqlite3.connect('SQL/attacks.db')
        cur = conn.cursor()

        cur.execute('''
        CREATE TABLE IF NOT EXISTS attacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            target TEXT,
            time INTEGER,
            method TEXT,
            active INTEGER,
            uid TEXT
        )''')

        conn.commit()
        conn.close()

        loaded += 1
    except Exception as e:
        print(f'{c.lred}[SQL] {c.reset}Database error: {c.lred} [ attacks.db - {e}]{c.reset}')


    try:
        conn = sqlite3.connect('SQL/keys.db')
        cur = conn.cursor()

        cur.execute('''
        CREATE TABLE IF NOT EXISTS keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT,
            plan TEXT,
            active INTEGER
        )''')

        conn.commit()
        conn.close()

        loaded += 1
    except Exception as e:
        print(f'{c.lred}[SQL] {c.reset}Database error: {c.lred} [ keys.db - {e}]{c.reset}')

    print(f'{c.dblue}[SQL] {c.reset}Correctly Loaded {c.dblue}{loaded} {c.reset}databases')