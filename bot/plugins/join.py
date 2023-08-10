from pyrogram import filters
from bot import on_call, kreacher
from pyrogram.enums.chat_type import ChatType
from bot.instance_of.every_vc import VOICE_CHATS


@kreacher.on_message(filters.regex(pattern="^[!?/]join"))
async def _(client, message):
    user = await kreacher.get_chat_member(
        message.chat.id, message.from_user.id
    )
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply(
            "**__Mr. Wizard, this command can only be used in groups or channels__** \U0001f937\U0001f3fb\u200D\u2642\uFE0F"
        )
    if not user.privileges.can_manage_chat:
        return await message.reply(
            "**__You are not my master, you do not order me what to do, bye__** \U0001f621"
        )
    try:
        chat = message.chat
        if VOICE_CHATS.get(chat.id) is not None:
            raise Exception("Streaming is active")
        await on_call.join(chat.id)
        VOICE_CHATS[chat.id] = on_call
        await message.reply(
            "**__Master, what do you need? \U0001f917 \n\nVoice Chat started successfully__** \u2728",
        )
    except Exception as e:
        return await message.reply(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
