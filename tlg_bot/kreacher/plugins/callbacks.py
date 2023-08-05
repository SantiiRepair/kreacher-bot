from kreacher import kreacher
from kreacher.dicts.dicts import VOICE_CHATS
from telethon import events


@kreacher.on(events.callbackquery.CallbackQuery(data="cls"))
async def _(event):
    await event.delete()


@kreacher.on(events.callbackquery.CallbackQuery(data="pause_callback"))
async def _(event):
    chat = await event.get_chat()
    proto = VOICE_CHATS[chat.id]
    await proto.set_pause(True)


@kreacher.on(events.callbackquery.CallbackQuery(data="resume_callback"))
async def _(event):
    chat = await event.get_chat()
    proto = VOICE_CHATS[chat.id]
    await proto.set_pause(False)


@kreacher.on(events.callbackquery.CallbackQuery(data="end_callback"))
async def _(event):
    chat = await event.get_chat()
    proto = VOICE_CHATS[chat.id]
    await proto.stop_media()
    VOICE_CHATS.pop(chat.id)
