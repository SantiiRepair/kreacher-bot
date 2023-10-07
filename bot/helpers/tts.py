import os
import uuid
import logging
from bot.helpers.bash import bash
from bot.utils.piper import get_model

c = os.path.dirname(os.path.abspath(__file__))
models = os.path.join(c, "../models")
tmp = os.path.join(c, "../tmp")


async def tts(text: str, output_file: str):
    model = get_model()
    try:
        if not os.path.exists(models):
            os.makedirs(models)
        elif not os.path.exists(os.path.dirname(output_file)):
            os.makedirs(os.path.dirname(output_file))
        elif not os.path.exists(tmp):
            os.makedirs(tmp)
        tmpf = f"{tmp}/{uuid.uuid4()}.txt"
        with open(tmpf, "w") as temp_text:
            temp_text.write(text)
            temp_text.close()
        await bash(
            f"piper -m {model} --download-dir {models} --data-dir {models} -f {output_file} < {tmpf}"
        )
        os.remove(tmpf)
    except Exception as e:
        logging.error(e)
        raise e
