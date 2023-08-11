from bot import kreacher
from pyrogram import filters
from pyrogram.enums.chat_type import ChatType
from bot.helpers.queues import clear_queue
from bot.instance_of.every_vc import VOICE_CHATS


@kreacher.on_message(filters.regex(pattern="^[!?/]leave"))
async def _(client, message):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply(
            "**__Mr. Wizard, this command can only be used in groups or channels__** \U0001f937\U0001f3fb\u200D\u2642\uFE0F"
        )
    user = await kreacher.get_chat_member(
        message.chat.id, message.from_user.id
    )
    if not user.privileges:
        return await message.reply(
            "**__You are not my master, you do not order me what to do, bye__** \U0001f621"
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
