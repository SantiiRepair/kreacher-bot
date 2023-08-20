import logging
from translate import Translator


async def translator(text: str, to_lang: str):
    try:
        translator = Translator(to_lang=to_lang)
        return translator.translate(text)
    except Exception as e:
        logging.error(e)
        raise e
