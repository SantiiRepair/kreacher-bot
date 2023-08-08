from bot import on_call, kreacher
from bot.instance_of.every_vc import VOICE_CHATS


@kreacher.on_message(filters.regex(pattern="^[!?/]new"))
async def _(client, message):
    try:
        chat = await message.chat
        if VOICE_CHATS.get(chat.id) is not None:
            raise Exception("Streaming is active")
        await on_call.start(chat.id)
        VOICE_CHATS[chat.id] = on_call
        await message.reply(
            "__Master, what do you need? \n\nVoice Chat started successfully.__",
        )
    except Exception as e:
        return await message.reply(
            f"__Oops master, something wrong has happened.__ \n\n`Error: {e}`",
        )
