from pyrogram.types import Message
from pyrogram import filters, Client
from bot import kreacher, VOICE_CHATS
from bot.helpers.queues import remove_queue
from bot.decorators.only_admins import only_admins
from bot.decorators.only_grps_chnns import only_grps_chnns


@kreacher.on_message(filters.regex(pattern="^[!?/]leave"))
@only_grps_chnns
@only_admins
async def _(client: Client, message: Message):
    try:
        if VOICE_CHATS.get(message.chat.id) is None:
            raise Exception("No streams")
        await VOICE_CHATS[message.chat.id].leave_current_group_call()
        VOICE_CHATS.pop(message.chat.id)
        remove_queue(str(message.chat.id))
        await message.reply(
            "**__Goodbye master, just call me if you need me \U0001FAE1 \n\nVoice Chat left successfully__** \u2728",
        )
    except Exception as e:
        return await message.reply(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
