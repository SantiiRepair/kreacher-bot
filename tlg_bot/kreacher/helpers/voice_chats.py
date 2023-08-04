import pickle
from kreacher import client
from pytgcalls import GroupCallFactory

VOICE_CHATS_FILE = "voice_chats.pkl"


def load_voice_chats():
    try:
        with open(VOICE_CHATS_FILE, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}


def save_voice_chats(voice_chats):
    with open(VOICE_CHATS_FILE, "wb") as file:
        pickle.dump(voice_chats, file)


async def create_voice_chat(chat_id):
    _factory = GroupCallFactory(
        client, GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON)
    voice_chat = _factory.get_group_call()

    voice_chats = load_voice_chats()
    current = voice_chats.get(chat_id)

    if current is not None:
        raise Exception("I'm joined in the Voice Chat")

    voice_chats[chat_id] = voice_chat
    save_voice_chats(voice_chats)


async def get_voice_chat(chat_id):
    voice_chats = load_voice_chats()
    voice_chat = voice_chats.get(chat_id)

    return voice_chat


async def stop_voice_chat(chat_id):
    voice_chats = load_voice_chats()
    voice_chat = voice_chats.get(chat_id)

    if voice_chat is None:
        raise Exception("Streaming is not started")

    del voice_chats[chat_id]
    save_voice_chats(voice_chats)
