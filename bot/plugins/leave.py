from bot import kreacher
from pyrogram import filters, Client
from pyrogram.types import Message
from bot.decorators.cmdp import cmd_protected
from pyrogram.enums.chat_type import ChatType
from bot.helpers.queues import clear_queue
from bot.dbs.instances import VOICE_CHATS


@kreacher.on_message(filters.regex(pattern="^[!?/]leave"))
@cmd_protected
async def _(client: Client, message: Message):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply(
            "**__Mr. Wizard, this command can only be used in groups or channels__** \U0001f937\U0001f3fb\u200D\u2642\uFE0F"
        )
    try:
        chat = message.chat
        if VOICE_CHATS.get(chat.id) is None:
            raise Exception("Streaming is not active")
        await VOICE_CHATS[chat.id].leave_current_group_call()
        VOICE_CHATS.pop(chat.id)
        await clear_queue(chat)
        await message.reply(
            "**__Goodbye master, just call me if you need me \U0001FAE1 \n\nVoice Chat left successfully__** \u2728",
        )
    except Exception as e:
        return await message.reply(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
