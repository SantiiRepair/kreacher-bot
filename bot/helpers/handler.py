import os
import pickle
from bot.helpers.pkl import load_pkl, dump_pkl
from bot.instance_of.every_vc import VOICE_CHATS
from bot.helpers.queues import clear_queue, get_queue, pop_an_item

dir = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(dir, "../dbs/queues.pkl")
actives = os.path.join(dir, "../dbs/actives.pkl")


async def skip_current(chat):
    QUEUE = load_pkl(queues, "rb", "dict")
    if chat.id not in QUEUE:
        return 0
    chat_queue = get_queue(chat)
    if len(chat_queue) == 1:
        await VOICE_CHATS[chat.id].stop_video()
        await VOICE_CHATS[chat.id].stop()
        clear_queue(chat)
        VOICE_CHATS.pop(chat.id)
        ACTIVE = load_pkl(actives, "rb", "list")
        ACTIVE.remove(chat.id)
        dump_pkl(actives, "wb", ACTIVE)
        return 1
    name = chat_queue[1][0]
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
    return [name, link, type]


async def next_item(chat, x: int):
    QUEUE = load_pkl(queues, "rb", "dict")
    if chat.id not in QUEUE:
        return 0
    chat_queue = get_queue(chat)
    try:
        name = chat_queue[x][0]
        chat_queue.pop(x)
        dump_pkl(queues, "wb", chat_queue)
        return name
    except Exception as e:
        print(e)
        return 0
