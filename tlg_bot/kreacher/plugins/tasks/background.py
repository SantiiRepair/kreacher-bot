from kreacher import ins
from pytgcalls.types import Update
from kreacher.helpers.queues import (
    QUEUE,
    clear_queue,
    active,
)


@ins.on_stream_end()
async def stream_end_handler(_, u: Update):
    chat = u.get_chat()
    print(chat.id)
    await skip_current_song(chat.id)


@ins.on_closed_voice_chat()
async def closed(_, chat):
    if chat.id in QUEUE:
        clear_queue(chat.id)
    if chat.id in active:
        active.remove(chat.id)


@ins.on_left()
async def left(_, chat):
    if chat.id in QUEUE:
        clear_queue(chat.id)
    if chat.id in active:
        active.remove(chat.id)


@ins.on_kicked()
async def kicked(_, chat):
    if chat.id in QUEUE:
        clear_queue(chat.id)
    if chat.id in active:
        active.remove(chat.id)
