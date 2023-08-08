from bot import kreacher
from pyrogram import filters
from bot.helpers.queues import clear_queue
from bot.instance_of.every_vc import VOICE_CHATS


@kreacher.on_message(filters.regex(pattern="^[!?/]leave"))
async def _(client, message):
    try:
        chat = message.chat
        if VOICE_CHATS.get(chat.id) is None:
            raise Exception("Streaming is not active")
        await VOICE_CHATS[chat.id].leave_current_group_call()
        VOICE_CHATS.pop(chat.id)
        clear_queue(chat)
        await message.reply(
            "__Goodbye master, just call me if you need me. \n\nVoice Chat left successfully.__",
        )
    except Exception as e:
        return await message.reply(
            f"__Oops master, something wrong has happened.__ \n\n`Error: {e}`",
        )
