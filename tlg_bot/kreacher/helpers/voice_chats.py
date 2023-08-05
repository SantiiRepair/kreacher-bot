VOICE_CHATS = {}


def get_voice_chat(chat):
    return VOICE_CHATS.get(chat.id)


def start_voice_chat(chat, instance):
    VOICE_CHATS[chat.id] = instance


async def stop_voice_chat(chat):
    VOICE_CHATS.pop(chat.id)
