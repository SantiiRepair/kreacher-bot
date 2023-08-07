import os
import pickle
from bot.instance.of_every_vc import VOICE_CHATS
from bot.helpers.queues import (
    clear_queue,
    get_queue,
    pop_an_item,
    get_active_chats,
)

dir = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(dir, "../dbs/queues.pkl")
actives = os.path.join(dir, "../dbs/actives.pkl")


async def skip_current(chat):
    with open(queues, "r") as q:
        QUEUE = pickle.load(q)
    if chat.id not in QUEUE:
        return 0
    chat_queue = get_queue(chat)
    if len(chat_queue) == 1:
        await VOICE_CHATS[chat.id].stop_video()
        await VOICE_CHATS[chat.id].stop()
        clear_queue(chat)
        VOICE_CHATS.pop(chat.id)
        ACTIVE = await get_active_chats()
        ACTIVE.remove(chat.id)
        with open(actives, "w") as a:
            pickle.dump(ACTIVE, a)
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
    with open(queues, "r") as q:
        QUEUE = pickle.load(q)
    if chat.id not in QUEUE:
        return 0
    chat_queue = get_queue(chat)
    try:
        name = chat_queue[x][0]
        chat_queue.pop(x)
        with open(queues, "w") as q:
            pickle.dump(chat_queue, q)
        return name
    except Exception as e:
        print(e)
        return 0
