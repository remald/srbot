import math
from copy import copy
from datetime import datetime, timedelta

import aiohttp
from PIL import Image
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.bot import bot, dp, TR
import io
from util.live_options import __LIVE_OPTIONS__
from util import mq


async def send_bytes(user_id, bio):
    await bot.send_document(user_id, bio,
                            caption=TR("done"))


def get_bytearray(img: Image):
    bio = io.BytesIO()
    bio.name = 'image.png'
    img.save(bio, 'PNG', quality=100)
    return bio.getvalue()


@dp.message_handler(content_types=['photo', 'document'], state='*')
async def handle_docs_photo(message, state: FSMContext):
    print(message.from_user)
    if message.photo:
        link = await message.photo[-1].get_url()
        await message.answer(TR("send_as_doc"))
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
        await send_image(message, image, TR("downscaled"))

    await message.reply(TR("wait_task"))

    data = get_bytearray(image)
    await mq.publish_bytes(data, message.from_user.id, __LIVE_OPTIONS__.get_selected_model(message.from_user.id))


async def send_image(message: Message, image: Image, text: str):
    bio = io.BytesIO()
    bio.name = 'image.png'
    image.save(bio, 'PNG')
    bio.seek(0)
    await message.reply_document(copy(bio), caption=text)
    # await message.reply_photo(bio, caption=text)


async def oom(message: Message):
    td = timedelta(minutes=20)
    user_id = str(message.from_user.id)
    oom_time = __LIVE_OPTIONS__.get_oom_message_viewed(user_id)
    if oom_time is not None and oom_time - datetime.now() < td:
        return

    __LIVE_OPTIONS__.set_oom_message_viewed(user_id, datetime.now() + td)

    with open('resource/price.jpg', 'rb') as img:
        await message.reply_photo(img, caption=TR("look_at_this"))

    await message.answer(TR("ram_price"))
