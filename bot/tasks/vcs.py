import os
import logging
from bot import on_call


c = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(c, "../dbs/queues.pkl")
actives = os.path.join(c, "../dbs/actives.pkl")


@on_call.on_audio_playout_ended
async def audio_ended(gc, source):
    logging.info(f"audio ended: {source}")
    os.remove(source)


@on_call.on_video_playout_ended
async def video_ended(gc, source):
    logging.info(f"video ended: {source}")
    os.remove(source)
