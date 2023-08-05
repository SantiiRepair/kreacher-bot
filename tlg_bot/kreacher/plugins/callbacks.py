from kreacher import kreacher
from kreacher.helpers.voice_chats import get_voice_chat
from telethon import events


@kreacher.on(events.callbackquery.CallbackQuery(data="cls"))
async def _(event):
    await event.delete()


@kreacher.on(events.callbackquery.CallbackQuery(data="pause_callback"))
async def _(event):
    chat = await event.get_chat()
    proto = get_voice_chat(chat)
    await proto.set_pause(True)


@kreacher.on(events.callbackquery.CallbackQuery(data="resume_callback"))
async def _(event):
    chat = await event.get_chat()
    proto = get_voice_chat(chat)
    await proto.set_pause(False)


@kreacher.on(events.callbackquery.CallbackQuery(data="end_callback"))
async def _(event):
    chat = await event.get_chat()
    proto = get_voice_chat(chat)
    await proto.stop_media()