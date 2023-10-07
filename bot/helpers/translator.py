import logging
from translate import Translator


async def translator(text: str, to_lang: str):
    try:
        tr = Translator(to_lang=to_lang)
        return tr.translate(text)
    except Exception as e:
        logging.error(e)
        raise e
