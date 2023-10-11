import os
import logging
from bot import tgcalls


@tgcalls.on_audio_playout_ended
async def audio_ended(client, source):
    logging.info(f"audio ended: {source}")
    os.remove(source)


@tgcalls.on_video_playout_ended
async def video_ended(client, source):
    logging.info(f"video ended: {source}")
    os.remove(source)
