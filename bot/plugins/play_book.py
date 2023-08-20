import PyPDF3
import pyttsx3
import os
import uuid
from asyncio import sleep
import logging
from pyrogram import filters, Client
from pyrogram.types import Message
from bot import kreacher, on_call
from bot.helpers.progress import progress
from bot.dbs.instances import VOICE_CHATS
from pyrogram.enums.chat_type import ChatType
from bot.helpers.queues import (
    add_to_queue,
    clear_queue,
)

current_dir = os.path.dirname(os.path.abspath(__file__))


@kreacher.on_message(filters.regex(pattern="^[!?/]play_book"))
async def _(client: Client, message: Message):
    counter = 11
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
        pdf = await message.reply_to_message.download(
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
            print(text)
            if not os.path.exists(os.path.dirname(audiobook)):
                os.makedirs(os.path.dirname(audiobook))
            audiobook_file = open(audiobook, "wb")
            engine.save_to_file(text, audiobook_file)
            if VOICE_CHATS.get(message.chat.id) is None:
                await msg.edit("\U0001fa84 **__Joining the voice chat...__**")
                await on_call.join(message.chat.id)
                VOICE_CHATS[message.chat.id] = on_call
            await on_call.start_audio(audiobook, repeat=False)
            await msg.edit("**__Started audiobook__**")
            os.remove(audiobook)
            counter += 1
        #os.remove(book)
    except Exception as e:
        logging.error(e)
        await msg.edit(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
        if message.chat.id in VOICE_CHATS:
            await VOICE_CHATS[message.chat.id].stop()
            await clear_queue(message.chat)
            VOICE_CHATS.pop(message.chat.id)
