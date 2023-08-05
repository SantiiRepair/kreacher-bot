from kreacher import kreacher
from kreacher.dicts.dicts import VOICE_CHATS
from telethon import events


@kreacher.on(events.callbackquery.CallbackQuery(data="cls"))
async def _(event):
    await event.delete()


@kreacher.on(events.callbackquery.CallbackQuery(data="pause_callback"))
async def _(event):
    chat = await event.get_chat()
    await VOICE_CHATS[chat.id].set_pause(True)


@kreacher.on(events.callbackquery.CallbackQuery(data="resume_callback"))
async def _(event):
    chat = await event.get_chat()
    await VOICE_CHATS[chat.id].set_pause(False)


@kreacher.on(events.callbackquery.CallbackQuery(data="end_callback"))
async def _(event):
    chat = await event.get_chat()
    await VOICE_CHATS[chat.id].stop_media()
