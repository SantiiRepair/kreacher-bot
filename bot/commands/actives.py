from asyncio import sleep
from pyrogram.types import Message
from pyrogram import filters, Client
from bot import kreacher, VOICE_CHATS
from bot.decorators.permissions import only_dev


@kreacher.on_message(filters.regex(pattern="^[!?/]actives"))
@only_dev
async def _(client: Client, message: Message):
    msg = await message.reply(
        "**__Getting active Voice Chats... \n\nPlease hold, master__**",
    )
    await sleep(2)
    served_chats = len(VOICE_CHATS)
    if served_chats > 0:
        return await msg.edit(
            f"**__Active Voice Chats:__** **{served_chats}**",
        )

    return await msg.edit("**__No active Voice Chats__**")
