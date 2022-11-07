import sqlite3 as sq
from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect('slang_dict.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK')
    base.execute('CREATE TABLE IF NOT EXISTS dictionary(name TEXT PRIMARY KEY, description TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO dictionary VALUES (?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM dictionary').fetchall():
        await bot.send_message(message.from_user.id, f'*Слово:* {ret[0]}\n*Определение:* {ret[1]}',
                               parse_mode="Markdown")


async def sql_delete_command(data):
    cur.execute('DELETE FROM dictionary WHERE name == ?', (data,))
    base.commit()


async def sql_read2():
    return cur.execute('SELECT * FROM dictionary').fetchall()


async def sql_send_def(message, word):
    desc = cur.execute('SELECT description FROM dictionary WHERE name == ?', (word,)).fetchone()
    if desc:
        for ret in desc:
            await bot.send_message(message.from_user.id, f'*{word}*\n\n{ret}', parse_mode="Markdown")
    # for ret in cur.execute('SELECT description FROM dictionary WHERE name == ?', (word,)).fetchone():
    #     await bot.send_message(message.from_user.id, f'*{word}*\n\n{ret}', parse_mode="Markdown")
    else:
        await bot.send_message(message.from_user.id, f'Слова *{word}* нет в словаре', parse_mode="Markdown")
