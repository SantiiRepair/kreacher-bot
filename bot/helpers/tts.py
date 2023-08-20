import os
from gtts import gTTS


async def tts(text, path, lang="en", slow=False):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    gtts = gTTS(text=text, lang=lang, slow=slow)
    gtts.save(path)
