from bot import kreacher
from asyncio import sleep
from bot.instance_of.every_vc import VOICE_CHATS


@kreacher.on_message(filters.regex(pattern="^[!?/]actives"))
async def _(client, message):
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
