import asyncio
import io
import logging
import math
from copy import copy
from datetime import datetime, timedelta

import aiohttp
from PIL import Image
from aio_pika import connect, Message, IncomingMessage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import __CONFIG__
from liveOptions import __LIVE_OPTIONS__
from lang.translation import translate, set_lang

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=__CONFIG__['token'])
dp = Dispatcher(bot, storage=MemoryStorage())

mq_chan = None


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    set_lang(message)
    button_self_trained = KeyboardButton('/self_trained_esrgan')
    button_xintao = KeyboardButton('/original_esrgan')

    greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    greet_kb.add(button_self_trained)
    greet_kb.add(button_xintao)
    await message.reply(translate(message.from_user.id)['MESSAGES']['start'],
                        reply_markup=greet_kb)


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    set_lang(message)
    await message.reply(translate(message.from_user.id)['MESSAGES']['help'])


@dp.message_handler(commands=['self_trained_esrgan'])
async def select_self_trained_model(message: types.Message):
    set_lang(message)
    __LIVE_OPTIONS__.set_selected_model(message.from_user.id, 'self')
    await message.reply(translate(message.from_user.id)["MESSAGES"]["self_selected"])


@dp.message_handler(commands=['original_esrgan'])
async def select_original_model(message: types.Message):
    set_lang(message)
    __LIVE_OPTIONS__.set_selected_model(message.from_user.id, 'xintao')
    await message.reply(translate(message.from_user.id)["MESSAGES"]["orig_selected"])


@dp.message_handler(regexp='(ты( у меня | и правда | )(умняша|умный))')
async def ama_smart_and_i_know_it(message: types.Message):
    await message.reply("я знаю! :3\n")


def get_bytearray(img: Image):
    bio = io.BytesIO()
    bio.name = 'image.png'
    img.save(bio, 'PNG', quality=100)
    return bio.getvalue()


async def get_result(message: IncomingMessage):
    bio = io.BytesIO(message.body)
    bio.seek(0)
    bio.name = 'uncompressed.png'
    await bot.send_document(message.headers['user_id'], bio,
                            caption=translate(message.headers['user_id'])['MESSAGES']['done'])


@dp.message_handler(content_types=['photo', 'document'], state='*')
async def handle_docs_photo(message, state: FSMContext):
    set_lang(message)
    print(message.from_user)
    if message.photo:
        link = await message.photo[-1].get_url()
        await message.answer(translate(message.from_user.id)['MESSAGES']['send_as_doc'])
    else:
        link = await message.document.get_url()
    async with aiohttp.ClientSession() as sess:
        async with sess.get(link) as response:
            image = Image.open(io.BytesIO(await response.read()))
    image.save("temp/" + f"{message.from_user['username']}_{datetime.now().strftime('%H:%M:%S')}" + ".jpg", "JPEG")

    if image.width * image.height > 256 * 256:
        await oom(message)
        ratio = math.sqrt(image.width * image.height / (256 * 256))
        image = image.resize((round(image.width / ratio) - 1, round(image.height / ratio) - 1), Image.BICUBIC)
        await send_image(message, image, translate(message.from_user.id)['MESSAGES']['downscaled'])

    await message.reply(translate(message.from_user.id)['MESSAGES']['wait_task'])

    data = get_bytearray(image)
    await mq_chan.default_exchange.publish(
        Message(data, headers={'user_id': message.from_user.id,
                               'model': __LIVE_OPTIONS__.get_selected_model(message.from_user.id)}),
        routing_key='process'
    )


async def send_image(message: types.Message, image: Image, text: str):
    bio = io.BytesIO()
    bio.name = 'image.png'
    image.save(bio, 'PNG')
    bio.seek(0)
    await message.reply_document(copy(bio), caption=text)
    # await message.reply_photo(bio, caption=text)


async def oom(message: types.Message):
    td = timedelta(minutes=20)
    user_id = str(message.from_user.id)
    oom_time = __LIVE_OPTIONS__.get_oom_message_viewed(user_id)
    if oom_time is not None and oom_time - datetime.now() < td:
        return

    __LIVE_OPTIONS__.set_oom_message_viewed(user_id, datetime.now() + td)

    with open('resource/price.jpg', 'rb') as img:
        await message.reply_photo(img, caption=translate(message.from_user.id)['MESSAGES']['look_at_this'])

    await message.answer(translate(message.from_user.id)['MESSAGES']['ram_price'])


@dp.message_handler()
async def misunderstood(message: types.Message):
    set_lang(message)

    await message.answer(translate(message.from_user.id)['MESSAGES']['misunderstood'])


async def mq_thread(loop):
    global mq_chan

    mq_conn = await connect(
        "amqp://guest:guest@localhost/", loop=loop
    )
    # Creating a channel
    mq_chan = await mq_conn.channel()

    # Declaring queue
    queue = await mq_chan.declare_queue("result")

    await queue.consume(get_result, no_ack=True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mq_thread(loop))
    executor.start_polling(dp, skip_updates=True, loop=loop)
    loop.run_forever()
