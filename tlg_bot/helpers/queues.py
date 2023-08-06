import os
from pysondb import db
from tlg_bot.dicts.dicts import QUEUE

active = []

dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(dir, "../dbs/queues.json")
dbq = db.getDb(path)


async def get_active_chats() -> list:
    return active


def add_to_queue(chat, name, url, ref, type):
    queue = dbq.getByQuery({"chat_id": chat.id})
    try:
        if queue is not None:
            dbq.updateByQuery(
                {"chat_id": chat.id},
                queue.append({}),
            )
            return int(len(queue[0].get("chat_id")) - 1)
        if chat.id not in active:
            active.append(chat.id)
            dbq.add(
                {
                    "chat_id": chat.id,
                    "name": name,
                    "url": url,
                    "ref": ref,
                    "type": type,
                }
            )
    except Exception as e:
        raise e

    QUEUE[chat.id] = [[name, url, ref, type]]


def get_queue(chat):
    queue = dbq.getByQuery({"chat_id": chat.id})
    if queue[0] is not None:
        if queue in QUEUE:
            return QUEUE[chat.id]
        return 0


def pop_an_item(chat):
    if chat.id not in QUEUE:
        return 0
    chat_queue = QUEUE[chat.id]
    chat_queue.pop(0)
    return 1


def clear_queue(chat):
    if chat.id not in QUEUE:
        return 0
    QUEUE.pop(chat.id)
    if chat.id in active:
        active.remove(chat.id)
    return 1
