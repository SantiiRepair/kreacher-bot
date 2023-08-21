import os
import logging
from bot.helpers.bash import bash
from bot.helpers.translator import translator

current_dir = os.path.dirname(os.path.abspath(__file__))
models = os.path.join(current_dir, "../models")


async def tts(text: str, path: str, to_lang="", lang="en_us"):
    mdn = ""
    match lang.lower():
        case "en_us":
            mdn += "en_US-amy-medium"
        case "en_gb":
            mdn += "en_GB-alba-medium"
        case "es_es":
            mdn += "es_ES-davefx-medium"
        case "es_mx":
            mdn += "es_MX-ald-medium"
        case "fr_fr":
            mdn += "fr_FR-siwis-medium"
        case "pt_br":
            mdn += "pt_BR-faber-medium"
        case "pt_pt":
            mdn += "pt_PT-tugão-medium"
        case "ru_ru":
            mdn += "ru_RU-irina-medium"
    try:
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        if to_lang:
            translation = await translator(text, to_lang)
            await bash(
                f"echo '{translation}' | piper --download-dir {models} --model {mdn} --output_file {path}"
            )
            return
        print(f"echo '{text}' | piper --download-dir {models} --model {mdn} --output_file {path}")
        await bash(
            f"echo '{text}' | piper --download-dir {models} --model {mdn} --output_file {path}"
        )
    except Exception as e:
        logging.error(e)
        raise e
