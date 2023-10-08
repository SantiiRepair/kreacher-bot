import os
import logging
from bot import kreacher
from pyrogram.types import Message
from pyrogram import filters, Client
from bot.decorators.only_dev import only_dev


@kreacher.on_message(filters.regex(pattern="^[!?/]logs"))
@only_dev
async def _(client: Client, message: Message):
    try:
        c = os.path.dirname(os.path.abspath(__file__))
        document = os.path.join(c, "../../logs/logs.log")
        await message.reply_document(document=document)
    except Exception as e:
        logging.error(e)
        await message.reply(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
