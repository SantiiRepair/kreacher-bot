from kreacher import client
from pytgcalls import GroupCallFactory
VOICE_CHATS = {}


async def create_voice_chat(chat_id):
    _factory = GroupCallFactory(
        client, GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON)
    voice_chat = _factory.get_group_call()
    current = VOICE_CHATS.get(chat_id)
    if current is not None:
        raise Exception("I'am joined in the Voice Chat")
    else:
        VOICE_CHATS[chat_id] = voice_chat
        return True


async def get_voice_chat(chat_id):
    voice_chat = VOICE_CHATS.get(chat_id)
    if voice_chat is None:
        raise Exception("Streaming is not started")
    else:
        return voice_chat

async def stop_voice_chat(chat_id):
    voice_chat = VOICE_CHATS.get(chat_id)
    if voice_chat is None:
        raise Exception("Streaming is not started")
    else:
        del VOICE_CHATS[chat_id]
        return True

