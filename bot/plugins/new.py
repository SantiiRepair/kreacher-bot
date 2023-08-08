from bot import on_call, kreacher
from bot.instance_of.every_vc import VOICE_CHATS
from telethon import events


@kreacher.on(events.NewMessage(pattern="[!?/]new"))
async def new_handler(event):
    try:
        chat = await event.get_chat()
        if VOICE_CHATS.get(chat.id) is not None:
            raise Exception("Streaming is active")
        await on_call.start(chat.id)
        VOICE_CHATS[chat.id] = on_call
        await event.reply(
            "__Master, what do you need? \n\nVoice Chat started successfully.__",
        )
    except Exception as e:
        return await event.reply(
            f"__Oops master, something wrong has happened.__ \n\n`Error: {e}`",
        )
