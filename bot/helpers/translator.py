from translate import Translator


async def translator(text: str, to_lang: str):
    translator = Translator(to_lang=to_lang)
    return translator.translate(text)
