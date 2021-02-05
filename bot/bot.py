from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message

from util.config import __CONFIG__

# Initialize bot and dispatcher
bot = Bot(token=__CONFIG__['token'])
dp = Dispatcher(bot, storage=MemoryStorage())


def run_bot(loop):
    print('starting polling...')
    executor.start_polling(dp, skip_updates=True, loop=loop)
