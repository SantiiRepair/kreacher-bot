import PyPDF3
import pyttsx3
import os
import re
import uuid
from asyncio import sleep
import logging
from pyrogram import filters, Client
from pyrogram.types import Message
from bot import assistant, kreacher, on_call
from bot.config import config
from bot.helpers.progress import progress
from pyrogram.enums import MessagesFilter
from bot.dbs.instances import VOICE_CHATS
from pyrogram.enums.chat_type import ChatType
from bot.helpers.queues import (
    add_to_queue,
    clear_queue,
)

current_dir = os.path.dirname(os.path.abspath(__file__))


@kreacher.on_message(filters.regex(pattern="^[!?/]play_book"))
async def _(client: Client, message: Message):
    counter = 0
    engine = pyttsx3.init()
    book = os.path.join(
        current_dir, f"../downloads/books/{str(uuid.uuid4())}.pdf"
    )
    try:
        if message.chat.type == ChatType.PRIVATE:
            return await message.reply(
                "**__Mr. Wizard, this command can only be used in groups or channels__** \U0001f937\U0001f3fb\u200D\u2642\uFE0F"
            )
        if not message.reply_to_message:
            return await message.reply(
                "**__How to use this command.\n\nNext we show two ways to use this command, click on the button with the mode you are looking for to know details.__**"
            )
        msg = await message.reply("**__Searching...__**")
        await sleep(2)
        await msg.edit("\U0001f4be **__Downloading...__**")
        pdf = await message.download(
            file_name=book,
            progress=progress,
            progress_args=(client, message.chat, msg),
        )
        book_file = open(pdf, "rb")
        pdfRead = PyPDF3.PdfFileReader(book_file)
        while counter <= pdfRead.numPages:
            audiobook = os.path.join(
                current_dir, f"../downloads/audiobooks/{str(uuid.uuid4())}.mp3"
            )
            page = pdfRead.getPage(counter)
            text = page.extractText()
            engine.save_to_file(text, audiobook)
            await on_call.start_audio(audiobook, repeat=False)
            VOICE_CHATS[message.chat.id] = on_call
            os.remove(audiobook)
            counter += 1
        os.remove(book)
    except Exception as e:
        logging.error(e)
        await msg.edit(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
        if message.chat.id in VOICE_CHATS:
            await VOICE_CHATS[message.chat.id].stop()
            await clear_queue(message.chat)
            VOICE_CHATS.pop(message.chat.id)
