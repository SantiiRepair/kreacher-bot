import os
import pickle

active = []
dir = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(dir, "../dbs/queues.pkl")
actives = os.path.join(dir, "../dbs/actives.pkl")


async def get_active_chats() -> list:
    return active


def add_to_queue(chat, name, url, ref, type):
    with open(queues, "r+") as f:
        QUEUE = pickle.load(f)
    try:
        if chat.id in QUEUE:
            QUEUE[chat.id].append([name, url, ref, type])
            pickle.dump(QUEUE[chat.id], f)
            return int(len(QUEUE[chat.id]) - 1)
        if chat.id not in active:
            active.append(chat.id)
        QUEUE[chat.id] = [[name, url, ref, type]]
    except Exception as e:
        raise e


def get_queue(chat):
    with open(queues, "r") as f:
        QUEUE = pickle.load(f)
    try:
        if chat.id in QUEUE:
            return QUEUE[chat.id]
        return 0
    except Exception as e:
        raise e


def pop_an_item(chat):
    with open(queues, "r+") as f:
        QUEUE = pickle.load(f)
    try:
        if chat.id not in QUEUE:
            return 0
        QUEUE[chat.id].pop(0)
        pickle.dump(QUEUE)
        return 1
    except Exception as e:
        raise e


def clear_queue(chat):
    with open(queues, "r+") as f:
        QUEUE = pickle.load(f)
    try:
        if chat.id not in QUEUE:
            return 0
        QUEUE.pop(chat.id)
        pickle.dump(QUEUE)
        if chat.id in active:
            active.remove(chat.id)
        return 1
    except Exception as e:
        raise e
