from asyncio import sleep
from telethon import events
from bot import kreacher
from bot.instance_of.every_vc import VOICE_CHATS


@kreacher.on(events.NewMessage(pattern="[!?/]actives"))
async def actives(event):
    msg = await event.reply(
        "__Getting active Voice Chats... \n\nPlease hold, master__",
    )
    await sleep(3)
    served_chats = len(VOICE_CHATS)
    if served_chats > 0:
        return await msg.edit(
            f"__Active Voice Chats:__ **{served_chats}**",
        )

    return await msg.edit("__No active Voice Chats__")
