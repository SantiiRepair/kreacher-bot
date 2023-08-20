import os
import logging
from bot.helpers.bash import bash
from bot.helpers.translator import translator

current_dir = os.path.dirname(os.path.abspath(__file__))
models = os.path.join(current_dir, "../models")


async def tts(text: str, path: str, to_lang="", lang="en_us", slow=False):
    mdn = ""
    if lang.lower() == "en_us":
        mdn += "en_US-amy-medium"
    elif lang.lower() == "en_gb":
        mdn += "en_GB-alba-medium"
    elif lang.lower() == "es_es":
        mdn += "es_ES-davefx-medium"
    elif lang.lower() == "es_mx":
        mdn += "es_MX-ald-medium"
    elif lang.lower() == "fr_fr":
        mdn += "fr_FR-siwis-medium"
    elif lang.lower() == "pt_br":
        mdn += "pt_BR-faber-medium"
    elif lang.lower() == "pt_pt":
        mdn += "pt_PT-tugão-medium"
    elif lang.lower() == "ru_ru":
        mdn += "ru_RU-irina-medium"
    try:
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        if to_lang:
            translation = await translator(text, to_lang)
            await bash(
                f"echo '{translation}' | piper --model {mdn} --download-dir {models} --output_file {path}"
            )
            return
        await bash(
            f"echo '{text}' | piper --model {mdn} --download-dir {models} --output_file {path}"
        )
    except Exception as e:
        logging.error(e)
        raise e
