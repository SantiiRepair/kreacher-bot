import os
import logging
from bot import on_call


@on_call.on_audio_playout_ended
async def audio_ended(gc, source):
    logging.info(f"audio ended: {source}")
    os.remove(source)


@on_call.on_video_playout_ended
async def video_ended(gc, source):
    logging.info(f"video ended: {source}")
    os.remove(source)
