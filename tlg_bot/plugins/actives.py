from asyncio import sleep
from telethon import events
from kreacher import kreacher
from kreacher.dicts.dicts import VOICE_CHATS


@kreacher.on(events.NewMessage(pattern="[!?/]actives"))
async def actives(event):
    msg = await event.reply(
        "<i>Getting active Voice Chats... \n\nPlease hold, master</i>",
        parse_mode="HTML",
    )
    await sleep(3)
    served_chats = len(VOICE_CHATS)
    if served_chats > 0:
        return await msg.edit(
            f"<i>Active Voice Chats: </i><b>{served_chats}</b>",
            parse_mode="HTML",
        )

    return await msg.edit("<i>No active Voice Chats</i>", parse_mode="HTML")
