import os
from gtts import gTTS
from bot.helpers.translator import translator


async def tts(text: str, path: str, to_lang="", lang="en", slow=False):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    if to_lang:
        translation = await translator(text, to_lang)
        gtts = gTTS(text=translation, lang=lang, slow=slow)
        gtts.save(path)
        return
    gtts = gTTS(text=text, lang=lang, slow=slow)
    gtts.save(path)
