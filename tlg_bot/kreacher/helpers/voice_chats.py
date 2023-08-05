import pickle
from kreacher import client
from pytgcalls import GroupCallFactory

VOICE_CHATS_FILE = "voice_chats.pkl"

try:
    with open(VOICE_CHATS_FILE, "rb") as file:
        VOICE_CHATS = pickle.load(file)
except (FileNotFoundError, EOFError):
    VOICE_CHATS = {}


async def create_voice_chat(chat_id):
    factory = GroupCallFactory(client, GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON)
    voice_chat = factory.get_group_call()
    get = VOICE_CHATS.get(chat_id)
    if get is not None:
        raise Exception("I'm joined in the Voice Chat")

    VOICE_CHATS[chat_id] = voice_chat

    with open(VOICE_CHATS_FILE, "wb") as file:
        pickle.dump(VOICE_CHATS, file)


async def get_voice_chat(chat_id):
    voice_chat = VOICE_CHATS.get(chat_id)
    return voice_chat


async def stop_voice_chat(chat_id):
    voice_chat = VOICE_CHATS.get(chat_id)

    if voice_chat is None:
        raise Exception("Streaming is not started")

    del VOICE_CHATS[chat_id]

    with open(VOICE_CHATS_FILE, "wb") as file:
        pickle.dump(VOICE_CHATS, file)
