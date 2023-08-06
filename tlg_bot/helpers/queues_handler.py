from tlg_bot.dicts.dicts import QUEUE, VOICE_CHATS
from tlg_bot.helpers.queues import (
    clear_queue,
    get_queue,
    pop_an_item,
    active,
)


async def skip_current(chat):
    if chat.id not in QUEUE:
        return 0
    chat_queue = get_queue(chat)
    if len(chat_queue) == 1:
        await VOICE_CHATS[chat.id].stop_video()
        await VOICE_CHATS[chat.id].stop()
        clear_queue(chat)
        VOICE_CHATS.pop(chat.id)
        active.remove(chat.id)
        return 1
    songname = chat_queue[1][0]
    url = chat_queue[1][1]
    link = chat_queue[1][2]
    type = chat_queue[1][3]
    if type == "audio":
        await VOICE_CHATS[chat.id].start_audio(url, repeat=False)
    elif type == "video":
        await VOICE_CHATS[chat.id].start_video(
            url, with_audio=True, repeat=False
        )
    pop_an_item(chat)
    return [songname, link, type]


async def next_item(chat, x: int):
    if chat.id not in QUEUE:
        return 0
    chat_queue = get_queue(chat)
    try:
        name = chat_queue[x][0]
        chat_queue.pop(x)
        return name
    except Exception as e:
        print(e)
        return 0
