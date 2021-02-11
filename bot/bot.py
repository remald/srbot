from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram.types import Message
from typing import Any, Tuple

from util.config import __CONFIG__

# Initialize bot and dispatcher
bot = Bot(token=__CONFIG__['token'])
dp = Dispatcher(bot, storage=MemoryStorage())

I18N_DOMAIN = 'srbot'
LOCALES_DIR = 'i18n/locales'


class SrbotLocale(I18nMiddleware):

    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        data: dict = args[-1]
        print(self.default)
        if "chat" in data:
            return data["chat"].language or self.default
        return self.default


i18n = SrbotLocale(I18N_DOMAIN, LOCALES_DIR, default='en')
TR = i18n.gettext
dp.middleware.setup(i18n)


def run_bot(loop):
    print('starting polling...')
    executor.start_polling(dp, skip_updates=True, loop=loop)
