from bot import ins
from pytgcalls.types import Update
from bot.helpers.queues_handler import skip_current
from bot.dicts.dicts import QUEUE
from bot.helpers.queues import (
    clear_queue,
    active,
)


@ins.on_stream_end()
async def stream_end_handler(_, u: Update):
    chat = u.get_chat()
    await skip_current(chat)


@ins.on_closed_voice_chat()
async def closed(_, chat):
    if chat.id in QUEUE:
        clear_queue(chat)
    if chat.id in active:
        active.remove(chat.id)


@ins.on_left()
async def left(_, chat):
    if chat.id in QUEUE:
        clear_queue(chat)
    if chat.id in active:
        active.remove(chat.id)


@ins.on_kicked()
async def kicked(_, chat):
    if chat.id in QUEUE:
        clear_queue(chat)
    if chat.id in active:
        active.remove(chat.id)
