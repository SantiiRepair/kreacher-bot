from pyrogram.types import Message
from pyrogram import filters, client
from bot import on_call, kreacher, VOICE_CHATS
from bot.decorators.only_admins import only_admins
from bot.decorators.only_grps_chnns import only_grps_chnns


@kreacher.on_message(filters.regex(pattern="^[!?/]join"))
@only_grps_chnns
@only_admins
async def _(client: Client, message: Message):
    try:
        if VOICE_CHATS.get(message.chat.id) is not None:
            raise Exception("Streaming is active")
        await on_call.start(message.chat.id)
        VOICE_CHATS[message.chat.id] = on_call
        await message.reply(
            "**__Master, what do you need? \U0001f917 \n\nVoice Chat started successfully__** \u2728",
        )
    except Exception as e:
        return await message.reply(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
