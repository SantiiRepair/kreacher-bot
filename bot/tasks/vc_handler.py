import os
import pickle
from bot import on_call
from bot.helpers.handler import skip_current
from bot.helpers.queues import clear_queue, get_active_chats

current_dir = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(current_dir, "../dbs/queues.pkl")
actives = os.path.join(current_dir, "../dbs/actives.pkl")


@on_call.on_audio_playout_ended
async def audio_ended(gc, source):
    print(f"audio ended: {source}")


@on_call.on_video_playout_ended
async def video_ended(gc, source):
    print(f"video ended: {source}")


@on_call.on_playout_ended
async def media_ended(gc, source, media_type):
    print(f"{media_type} ended: {source}")
