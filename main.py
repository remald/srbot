"""
This is a echo bot.
It echoes any incoming text messages.
"""
import asyncio
import io
import logging
import math
import threading
from datetime import datetime, timedelta

from aio_pika.patterns import Master

from liveOptions import __LIVE_OPTIONS__

from PIL import Image
from aiogram.dispatcher import FSMContext

from config import __CONFIG__

import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from aio_pika import connect, Message, IncomingMessage

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=__CONFIG__['token'])
dp = Dispatcher(bot, storage=MemoryStorage())

mq_chan = None


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    button_self_trained = KeyboardButton('/self_trained_esrgan')
    button_xintao = KeyboardButton('/original_esrgan')

    greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    greet_kb.add(button_self_trained)
    greet_kb.add(button_xintao)
    await message.reply("Hi!\nI'm a newest AI system!\nI use deep learning to do some magic!"
                        " Give me a photo and the magic will happen! \nNOTE: max supported pix resolution is 256*256!\n",
                        reply_markup=greet_kb)


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("Supported commands:\n"
                        "/self_trained_esrgan - deep neural network for image super resolution, trained by me\n"
                        "/original_esrgan - esrgan pretrained by authors\n")


@dp.message_handler(commands=['self_trained_esrgan'])
async def select_self_trained_model(message: types.Message):
    __LIVE_OPTIONS__.set_selected_model(message.from_user.id, 'self')
    await message.reply("Self-trained model is selected!\n")


@dp.message_handler(commands=['original_esrgan'])
async def select_original_model(message: types.Message):
    __LIVE_OPTIONS__.set_selected_model(message.from_user.id, 'xintao')
    await message.reply("Original model is selected!\n")


@dp.message_handler(regexp='(ты( у меня | и правда | )(умняша|умный))')
async def select_original_model(message: types.Message):
    __LIVE_OPTIONS__.set_selected_model(message.from_user.id, 'xintao')
    await message.reply("я знаю! :3\n")


def get_bytearray(img: Image):
    bio = io.BytesIO()
    bio.name = 'image.png'
    img.save(bio, 'PNG', quality=100)
    return bio.getvalue()


async def get_result(message: IncomingMessage):
    bio = io.BytesIO(message.body)
    bio.seek(0)
    await bot.send_photo(message.headers['user_id'], bio, 'I did some magic 😺')


@dp.message_handler(content_types=['photo', 'document'], state='*')
async def handle_docs_photo(message, state: FSMContext):
    print(message.from_user)
    if message.photo:
        link = await message.photo[-1].get_url()
    else:
        link = await message.document.get_url()
    async with aiohttp.ClientSession() as sess:
        async with sess.get(link) as response:
            image = Image.open(io.BytesIO(await response.read()))
    print(image)
    image.save("temp/" + f"{message.from_user['username']}_{datetime.now().strftime('%H:%M:%S')}" + ".jpg", "JPEG")

    if image.width * image.height > 256 * 256:
        await oom(message)
        ratio = math.sqrt(image.width * image.height / (256 * 256))
        image = image.resize((round(image.width / ratio), round(image.height / ratio)), Image.BICUBIC)
        await send_image(message, image, "Downscaled image after bicubic resize (256 * 256 is max supported size)")

    await message.reply("Your picture is being processed now! This may take a while depending on the pic size.\n")

    data = get_bytearray(image)
    await mq_chan.default_exchange.publish(
        Message(data, headers={'user_id': message.from_user.id,
                               'model': __LIVE_OPTIONS__.get_selected_model(message.from_user.id)}),
        routing_key='process'
    )


async def send_image(message: types.Message, image: Image, text: str):
    bio = io.BytesIO()
    bio.name = 'image.jpeg'
    image.save(bio, 'JPEG')
    bio.seek(0)
    await message.reply_photo(bio, caption=text)


async def oom(message: types.Message):
    td = timedelta(minutes=20)
    user_id = str(message.from_user.id)
    if user_id in __LIVE_OPTIONS__.oom_message_viewed and \
            __LIVE_OPTIONS__.oom_message_viewed[user_id] - datetime.now() < td:
        return

    __LIVE_OPTIONS__.oom_message_viewed[user_id] = datetime.now() + td

    with open('resource/price.jpg', 'rb') as img:
        await message.reply_photo(img, caption='Well, look at this...')

    await message.answer(
        "RAM price is growing day by day. "
        "I am not getting enough funding from my Master to have enough memory to handle such large pictures. "
        "I could ask you to donate, but my Master forbids me. He says it's indecent. "
        "Now I will resize your image to fit 255 * 255 size.")


@dp.message_handler()
async def misunderstood(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer("You told me something weired")


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
