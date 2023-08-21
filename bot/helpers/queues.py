import os
from bot.helpers.pkl import load_pkl, dump_pkl

current_dir = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(current_dir, "../dbs/queues.pkl")
actives = os.path.join(current_dir, "../dbs/actives.pkl")


async def get_active_chats() -> list:
    ACTIVE = await load_pkl(actives, "rb", "list")
    return ACTIVE


async def add_to_queue(chat, name, url, ref, typeof):
    try:
        QUEUE = await load_pkl(queues, "rb", "dict")
        ACTIVE = await load_pkl(actives, "rb", "list")
        if chat.id in QUEUE:
            QUEUE[chat.id].append([name, url, ref, type])
            await dump_pkl(queues, "wb", QUEUE)
            return int(len(QUEUE[chat.id]) - 1)
        if chat.id not in ACTIVE:
            ACTIVE.append(chat.id)
            await dump_pkl(actives, "wb", ACTIVE)
        QUEUE[chat.id] = [[name, url, ref, typeof]]
        await dump_pkl(queues, "wb", QUEUE)
    except Exception as e:
        raise e


async def get_queue(chat):
    QUEUE = await load_pkl(queues, "rb", "dict")
    try:
        if chat.id in QUEUE:
            return QUEUE[chat.id]
        return 0
    except Exception as e:
        raise e


async def pop_an_item(chat):
    QUEUE = await load_pkl(queues, "rb", "dict")
    try:
        if chat.id not in QUEUE:
            return 0
        QUEUE[chat.id].pop(0)
        await dump_pkl(queues, "wb", QUEUE)
        return 1
    except Exception as e:
        raise e


async def clear_queue(chat):
    QUEUE = await load_pkl(queues, "rb", "dict")
    ACTIVE = await load_pkl(actives, "rb", "list")
    try:
        if chat.id not in QUEUE:
            return 0
        QUEUE.pop(chat.id)
        await dump_pkl(queues, "wb", QUEUE)
        if chat.id in ACTIVE:
            ACTIVE.remove(chat.id)
            await dump_pkl(actives, "wb", ACTIVE)
        return 1
    except Exception as e:
        raise e
