from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram.types import Message

from util.config import __CONFIG__

# Initialize bot and dispatcher
bot = Bot(token=__CONFIG__['token'])
dp = Dispatcher(bot, storage=MemoryStorage())

I18N_DOMAIN = 'srbot'
LOCALES_DIR = 'i18n/locales'


i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
TR = i18n.gettext
dp.middleware.setup(i18n)


def run_bot(loop):
    print('starting polling...')
    executor.start_polling(dp, skip_updates=True, loop=loop)
