from kreacher import ins, kreacher
from kreacher.helpers.voice_chats import get_voice_chat, start_voice_chat
from telethon import events


@kreacher.on(events.NewMessage(pattern="[!?/]join"))
async def join_handler(event):
    try:
        chat = await event.get_chat()
        proto = get_voice_chat(chat)
        if proto is not None:
            raise Exception("Streaming is active")
        start_voice_chat(chat, ins)
        await proto.join(chat)
        await event.reply("<i>Master, what do you need? \n\nVoice Chat joined successfully.</i>", parse_mode="HTML")
    except Exception as e:
        return await event.reply(f"<i>Oops master, something wrong has happened. \n\nError:</i> <code>{e}</code>", parse_mode="HTML")
