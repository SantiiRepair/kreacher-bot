import os
import logging
from bot import kreacher, config
from pyrogram import filters, Client
from pyrogram.types import Message


@kreacher.on_message(filters.regex(pattern="^[!?/]logs"))
async def _(client: Client, message: Message):
    try:
        dev = await client.get_users(config.MANTAINER)
        if not dev.id == message.from_user.id:
            return await message.reply(
                f"**__Only [{dev.first_name}](https://t.me/{dev.username}), can execute this command__** \U0001f6ab",
                disable_web_page_preview=True,
            )
        current_dir = os.path.dirname(os.path.abspath(__file__))
        document = os.path.join(current_dir, "../logs/logs.txt")
        await message.reply_document(document=document)
    except Exception as e:
        logging.error(e)
        await message.reply(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
