from aiogram import types, Dispatcher
from create_bot import dp, bot


# @dp.message_handler()
# async def echo_send(message: types.Message):
#     # with open('slang_dict.txt') as json_file:
#     #     data = json.load(json_file)
#     #     for p in data[message.text]:
#     #         await bot.send_message(message.from_user.id, p)


def register_handlers_other(dp: Dispatcher):
    # dp.register_message_handler(echo_send)
    pass
