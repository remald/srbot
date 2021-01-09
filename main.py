"""
This is a echo bot.
It echoes any incoming text messages.
"""
import io
import logging
from PIL import Image
from config import __CONFIG__

import aiohttp
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'BOT TOKEN HERE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=__CONFIG__['token'])
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    print("photo")

    link = await message.photo[-1].get_url()
    async with aiohttp.ClientSession() as sess:
        async with sess.get(link) as response:
            image = Image.open(io.BytesIO(await response.read()))
    print(image)

    if image.width * image.height > 256*256:
        await oom(message)
    else:
        bio = io.BytesIO()
        bio.name = 'image.jpeg'
        image.save(bio, 'JPEG')
        bio.seek(0)
        await message.reply_photo(bio, caption='Just get your photo back 😺')


async def oom(message: types.Message):
    await message.answer(
        "RAM price is growing day by day. "
        "I am not getting enough funding from my Master to have enough memory to handle such large pictures. "
        "I could ask you to donate, but my Master forbids me. He says it's indecent. " 
        "Please choose a picture with less resolution.")


@dp.message_handler()
async def misunderstood(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer("You told me something weired")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
