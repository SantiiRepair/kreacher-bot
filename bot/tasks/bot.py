import os
import pickle
from bot import ins
from pytgcalls.types import Update
from bot.helpers.handler import skip_current
from bot.helpers.queues import (
    clear_queue,
    active,
)

dir = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(dir, "../dbs/queues.pkl")


@ins.on_stream_end()
async def stream_end_handler(_, u: Update):
    chat = u.get_chat()
    await skip_current(chat)


@ins.on_closed_voice_chat()
async def closed(_, chat):
    with open(queues, "r") as q:
        QUEUE = pickle.load(q)
    if chat.id in QUEUE:
        clear_queue(chat)
    if chat.id in active:
        active.remove(chat.id)
        with open(actives, "w") as a:
            pickle.dump(active, a)


@ins.on_left()
async def left(_, chat):
    with open(queues, "r") as q:
        QUEUE = pickle.load(q)
    if chat.id in QUEUE:
        clear_queue(chat)
    if chat.id in active:
        active.remove(chat.id)
        with open(actives, "w") as a:
            pickle.dump(active, a)


@ins.on_kicked()
async def kicked(_, chat):
    with open(queues, "r") as q:
        QUEUE = pickle.load(q)
    if chat.id in QUEUE:
        clear_queue(chat)
    if chat.id in active:
        active.remove(chat.id)
        with open(actives, "w") as a:
            pickle.dump(active, a)
