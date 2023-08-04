from telethon import events
from kreacher import kreacher
from kreacher.helpers.queues import get_active_chats


@kreacher.on(events.NewMessage(pattern="^/active_voice"))
async def activevc(message):
    mystic = await message.reply("Getting active voice chats.. Please hold")
    served_chats = await get_active_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await message.client.get_entity(x)).title
        except Exception:
            title = "Private Group"
        if (await message.client.get_entity(x)).username:
            user = (await message.client.get_entity(x)).username
            text += f"{j + 1}.  [{title}](https://t.me/{user})[`{x}`]\n"
        else:
            text += f"{j + 1}. {title} [`{x}`]\n"
        j += 1
    if not text:
        await mystic.edit("No Active Voice Chats")
    else:
        await mystic.edit(f"**Active Voice Chats:-**\n\n{text}")
