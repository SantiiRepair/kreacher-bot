from kreacher.dicts.dicts import QUEUE
active = []


async def get_active_chats() -> list:
    return active


def add_to_queue(chat, name, url, ref, type, quality):
    if chat.id in QUEUE:
        chat_queue = QUEUE[chat.id]
        chat_queue.append([name, url, ref, type])
        return int(len(chat_queue) - 1)
    if chat.id not in active:
        active.append(chat.id)

    QUEUE[chat.id] = [[name, url, ref, type]]


def get_queue(chat):
    if chat.id in QUEUE:
        return QUEUE[chat.id]
    return 0


def pop_an_item(chat_id):
    if chat_id not in QUEUE:
        return 0
    chat_queue = QUEUE[chat_id]
    chat_queue.pop(0)
    return 1


def clear_queue(chat):
    if chat.id not in QUEUE:
        return 0
    QUEUE.pop(chat.id)
    if chat.id in active:
        active.remove(chat.id)
    return 1
