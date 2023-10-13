from pyrogram.types import Message
from pyrogram import filters, Client
from bot import tgcalls, kreacher, VOICE_CHATS
from bot.decorators.permissions import only_admins
from bot.decorators.sides import only_groups_or_channels


@kreacher.on_message(filters.regex(pattern="^[!?/]join"))
@only_groups_or_channels
@only_admins
async def _(client: Client, message: Message):
    try:
        if VOICE_CHATS.get(message.chat.id) is not None:
            raise Exception("Streaming is active")
        VOICE_CHATS[message.chat.id] = tgcalls.get_group_call()
        await VOICE_CHATS[message.chat.id].start(message.chat.id)
        await message.reply(
            "**__Master, what do you need? \U0001f917 \n\nVoice Chat started successfully__** \u2728",
        )
    except Exception as e:
        return await message.reply(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
