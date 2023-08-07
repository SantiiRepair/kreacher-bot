import os
import pickle

dir = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(dir, "../dbs/queues.pkl")
actives = os.path.join(dir, "../dbs/actives.pkl")


async def get_active_chats() -> list:
    with open(actives, "rb") as a:
        ACTIVE = pickle.load(a)
    return ACTIVE


def add_to_queue(chat, name, url, ref, type):
    with open(queues, "rb") as q:
        QUEUE = pickle.load(q)
    with open(actives, "rb") as a:
        ACTIVE = pickle.load(a)
    try:
        if chat.id in QUEUE:
            QUEUE[chat.id].append([name, url, ref, type])
            with open(queues, "wb") as q:
                pickle.dump(QUEUE, q)
            return int(len(QUEUE[chat.id]) - 1)
        if chat.id not in ACTIVE:
            ACTIVE.append(chat.id)
            with open(actives, "wb") as a:
                pickle.dump(ACTIVE, a)
        QUEUE[chat.id] = [[name, url, ref, type]]
        with open(queues, "wb") as q:
            pickle.dump(QUEUE, q)
    except Exception as e:
        raise e


def get_queue(chat):
    with open(queues, "rb") as q:
        QUEUE = pickle.load(f)
    try:
        if chat.id in QUEUE:
            return QUEUE[chat.id]
        return 0
    except Exception as e:
        raise e


def pop_an_item(chat):
    with open(queues, "rb") as q:
        QUEUE = pickle.load(q)
    try:
        if chat.id not in QUEUE:
            return 0
        QUEUE[chat.id].pop(0)
        with open(queues, "wb") as q:
            pickle.dump(QUEUE, q)
        return 1
    except Exception as e:
        raise e


def clear_queue(chat):
    with open(queues, "rb") as q:
        QUEUE = pickle.load(q)
    with open(actives, "rb") as a:
        ACTIVE = pickle.load(a)
    try:
        if chat.id not in QUEUE:
            return 0
        QUEUE.pop(chat.id)
        with open(queues, "wb") as q:
            pickle.dump(QUEUE, q)
        if chat.id in ACTIVE:
            ACTIVE.remove(chat.id)
            with open(actives, "rb") as a:
                pickle.dump(ACTIVE, a)
        return 1
    except Exception as e:
        raise e
