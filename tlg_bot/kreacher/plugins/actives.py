from asyncio import sleep
from telethon import events
from kreacher import kreacher
from kreacher.dicts.dicts import VOICE_CHATS


@kreacher.on(events.NewMessage(pattern="[!?/]actives"))
async def actives(event):
    msg = await event.reply("Getting active voice chats.. Please hold")
    await sleep(3)
    served_chats = len(VOICE_CHATS)
    if served_chats > 0:
        return await msg.edit(f"**Active Voice Chats:-**\n\n{served_chats}")

    return await msg.edit("No Active Voice Chats")
