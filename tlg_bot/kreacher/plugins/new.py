from kreacher import ins, kreacher
from kreacher.helpers.voice_chats import VOICE_CHATS
from telethon import events


@kreacher.on(events.NewMessage(pattern="[!?/]new"))
async def new_handler(event):
    try:
        chat = await event.get_chat()
        if VOICE_CHATS.get(chat.id) is not None:
            raise Exception("Streaming is active")
        await ins.start(chat.id)
        VOICE_CHATS[chat.id] = ins
        await event.reply("<i>Master, what do you need? \n\nVoice Chat joined successfully.</i>", parse_mode="HTML")
    except Exception as e:
        return await event.reply(f"<i>Oops master, something wrong has happened. \n\nError:</i> <code>{e}</code>", parse_mode="HTML")
