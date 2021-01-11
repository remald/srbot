"""
This is a echo bot.
It echoes any incoming text messages.
"""
import io
import logging
import math
from datetime import datetime

from PIL import Image
from aiogram.dispatcher import FSMContext
from torchvision import transforms

from config import __CONFIG__
import util
import torch

import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=__CONFIG__['token'])
dp = Dispatcher(bot, storage=MemoryStorage())

netG = util.load_esr_model('weight/esr.pth')
netG.eval()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm a newest AI system!\nI use deep learning to do some magic!"
                        " Give me a photo and the magic will happen! \nNOTE: max supported pix resolution is 256*256!\n")


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
        await send_image(message, image, "Downscaled image after bicubic resize")

    lr = transforms.ToTensor()(image).unsqueeze(0)
    fake = netG(lr).clamp_(0., 1)
    image = transforms.ToPILImage(mode='RGB')(fake[0])
    await send_image(message, image, 'I did some magic 😺')


async def send_image(message: types.Message, image: Image, text: str):
    bio = io.BytesIO()
    bio.name = 'image.jpeg'
    image.save(bio, 'JPEG')
    bio.seek(0)
    await message.reply_photo(bio, caption=text)


async def oom(message: types.Message):
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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
