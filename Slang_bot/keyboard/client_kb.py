from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Помощь')
b2 = KeyboardButton('Открыть словарь')
b3 = KeyboardButton('Слово')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

kb_client.add(b1).add(b2).insert(b3)