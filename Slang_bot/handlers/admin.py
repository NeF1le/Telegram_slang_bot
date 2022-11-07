from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboard import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ID = 974923385


class FSMAdmin(StatesGroup):
    name = State()
    description = State()


async def admin_command(message: types.Message):
    global ID
    if message.from_user.id == ID:
        await bot.send_message(message.from_user.id, 'Отправляем админскую панель...',
                               reply_markup=admin_kb.button_case_admin)
        await message.delete()


# Начало диалога загрузки нового слова в словаре
# @dp.message.handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.name.set()
        await message.reply('Загрузи слово')


# @dp.message_handler(state='*', commands='Отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Готово')


# Ловим первый ответ
# @dp.message.handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи определение')


# Ловим второй ответ
# @dp.message.handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text

        await sqlite_db.sql_add_command(state)
        await state.finish()


# @dp.callback_query_handler(Text(equals='del ', ignore_case=False))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace("del ", ""))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалено', show_alert=True)


# @dp.message_handler(commands='Удалить')
async def delete_word(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_message(message.from_user.id, f'Слово: {ret[0]}\nОпределение: {ret[1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup(). \
                                   add(InlineKeyboardButton(f'Удалить {ret[0]}', callback_data=f'del {ret[0]}')))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state='*', commands='Отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(admin_command, commands=['admin'])
    dp.register_message_handler(delete_word, commands=['Удалить'])
    dp.register_callback_query_handler(del_callback_run, Text(startswith='del ', ignore_case=True))
