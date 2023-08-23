import os
import logging
from bot.helpers.bash import bash
from bot.helpers.piper import get_model

c = os.path.dirname(os.path.abspath(__file__))
models = os.path.join(c, "../models")


async def tts(text: str, output_file: str):
    model = get_model()
    try:
        if not os.path.exists(models):
            os.makedirs(models)
        elif not os.path.exists(os.path.dirname(output_file)):
            os.makedirs(os.path.dirname(output_file))
        await bash(
            f"echo '{text}' | piper -m {model} --download-dir {models} --data-dir {models} -f {output_file}"
        )
    except Exception as e:
        logging.error(e)
        raise e
