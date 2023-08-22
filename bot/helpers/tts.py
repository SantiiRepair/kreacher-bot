import os
import logging
from bot.helpers.bash import bash

current_dir = os.path.dirname(os.path.abspath(__file__))
models = os.path.join(current_dir, "../models")


async def tts(text: str, path: str):
    voice = _get_voice()
    try:
        if not os.path.exists(models):
            os.makedirs(models)
        elif not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        await bash(
            f"echo '{text}' | piper -m {voice} --download-dir {models} --data-dir {models} -f {path}"
        )
    except Exception as e:
        logging.error(e)
        raise e


def _get_voice(lang="es_es", gender="female") -> str:
    mdn = ""
    if gender == "female":
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
        return mdn
    if gender == "male":
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
        return mdn
    return ValueError("Wrong country code, not found model")
