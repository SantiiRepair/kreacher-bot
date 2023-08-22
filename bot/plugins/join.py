from bot import on_call, kreacher
from pyrogram.types import Message
from pyrogram import filters, Client
from bot.dbs.instances import VOICE_CHATS
from pyrogram.enums.chat_type import ChatType
from bot.decorators.only_admins import only_admins
from bot.decorators.only_grps_chnns import only_grps_chnns


@kreacher.on_message(filters.regex(pattern="^[!?/]join"))
@only_grps_chnns
@only_admins
async def _(client: Client, message: Message):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply(
            "**__Mr. Wizard, this command can only be used in groups or channels__** \U0001f937\U0001f3fb\u200D\u2642\uFE0F"
        )
    try:
        if VOICE_CHATS.get(message.chat.id) is not None:
            raise Exception("Streaming is active")
        await on_call.join(message.chat.id)
        VOICE_CHATS[message.chat.id] = on_call
        await message.reply(
            "**__Master, what do you need? \U0001f917 \n\nVoice Chat started successfully__** \u2728",
        )
    except Exception as e:
        return await message.reply(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
