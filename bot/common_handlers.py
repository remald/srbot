from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message

from bot.bot import dp
from lang.translation import set_lang, translate
from util.liveOptions import __LIVE_OPTIONS__


@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    set_lang(message)
    button_self_trained = KeyboardButton('/self_trained_esrgan')
    button_original = KeyboardButton('/original_esrgan')

    greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    greet_kb.add(button_self_trained)
    greet_kb.add(button_original)
    await message.reply(translate(message.from_user.id)['MESSAGES']['start'],
                        reply_markup=greet_kb)


@dp.message_handler(commands=['help'])
async def send_help(message: Message):
    set_lang(message)
    await message.reply(translate(message.from_user.id)['MESSAGES']['help'])


@dp.message_handler(commands=['self_trained_esrgan'])
async def select_self_trained_model(message: Message):
    set_lang(message)
    __LIVE_OPTIONS__.set_selected_model(message.from_user.id, 'self')
    await message.reply(translate(message.from_user.id)["MESSAGES"]["self_selected"])


@dp.message_handler(commands=['original_esrgan'])
async def select_original_model(message: Message):
    set_lang(message)
    __LIVE_OPTIONS__.set_selected_model(message.from_user.id, 'original')
    await message.reply(translate(message.from_user.id)["MESSAGES"]["orig_selected"])


@dp.message_handler(regexp='(ты( у меня | и правда | )(умняша|умный))')
async def ama_smart_and_i_know_it(message: Message):
    await message.reply("я знаю! :3\n")


@dp.message_handler()
async def misunderstood(message: Message):
    set_lang(message)
    await message.answer(translate(message.from_user.id)['MESSAGES']['misunderstood'])
