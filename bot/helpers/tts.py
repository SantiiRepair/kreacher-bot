import os
import logging
from bot.helpers.piper import get_model, ptts

c = os.path.dirname(os.path.abspath(__file__))
models = os.path.join(c, "../models")


async def tts(text: str, output_file: str):
    model = get_model()
    try:
        if not os.path.exists(models):
            os.makedirs(models)
        elif not os.path.exists(os.path.dirname(output_file)):
            os.makedirs(os.path.dirname(output_file))
        await ptts(
            text=text,
            model=model,
            data_dir=models,
            download_dir=models,
            output_file=output_file,
            debug=True,
        )
    except Exception as e:
        logging.error(e)
        raise e
