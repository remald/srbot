
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from typing import Any, Tuple
from aiogram import types
from babel import Locale

SUPPORTED_LANGS = ['en', 'ru']


class SrbotLocale(I18nMiddleware):

    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        user: types.User = types.User.get_current()
        locale: Locale = user.locale
        language = None

        if locale:
            *_, data = args
            language = data['locale'] = locale.language
        return language if language in SUPPORTED_LANGS else self.default
