import lang.en as en
import lang.ru as ru
import liveOptions


def translate(client_id):
    lang = liveOptions.__LIVE_OPTIONS__.get_lang(client_id)
    if 'ru' in lang:
        tr = ru.translation
    else:
        tr = en.translation

    return tr


def set_lang(message):
    try:
        print(message.from_user.locale.language)
        liveOptions.__LIVE_OPTIONS__.set_lang(message.from_user.id, message.from_user.locale.language)
    except Exception:
        liveOptions.__LIVE_OPTIONS__.set_lang('en')
