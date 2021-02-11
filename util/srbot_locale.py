from aiogram.contrib.middlewares.i18n import I18nMiddleware
from typing import Any, Tuple


class SrbotLocale(I18nMiddleware):

    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        data: dict = args[-1]
        print(self.default)
        if "chat" in data:
            return data["chat"].language or self.default
        return self.default
