import PyPDF2
import os
import uuid
from asyncio import sleep
import logging
from pyrogram import filters, Client
from pyrogram.types import Message
from bot import kreacher, on_call
from bot.helpers.progress import progress
from bot.helpers.tts import tts
from bot.dbs.instances import VOICE_CHATS
from pyrogram.enums.chat_type import ChatType
from bot.helpers.queues import (
    add_to_queue,
    clear_queue,
)

current_dir = os.path.dirname(os.path.abspath(__file__))


@kreacher.on_message(filters.regex(pattern="^[!?/]play_book"))
async def _(client: Client, message: Message):
    text = ""
    book = os.path.join(
        current_dir, f"../downloads/books/{str(uuid.uuid4())}.pdf"
    )
    audiobook = os.path.join(
        current_dir, f"../downloads/audiobooks/{str(uuid.uuid4())}.mp3"
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
        msg = await message.reply("\u23F3 **__Processing...__**")
        await sleep(2)
        await msg.edit("\U0001f4be **__Downloading...__**")
        f = await message.reply_to_message.download(
            file_name=book,
            progress=progress,
            progress_args=(client, message.chat, msg),
        )
        pdf = PyPDF2.PdfReader(open(f, "rb"))
        if not " " in message.text:
            await msg.edit("**__Grouping pages...__**")
            for pgs in range(len(pdf.pages)):
                text += pdf.pages[pgs].extract_text()
            await msg.edit(f"**__{len(pdf.pages)} pages were grouped__**")
        elif " " in message.text:
            page_number = message.text.split(maxsplit=1)[1]
            if not page_number.isdigit():
                return await msg.edit("**__This is not a number__**")
            text += pdf.pages[int(page_number)].extract_text()
        await sleep(2)
        await msg.edit("**__Generating an audiobook__**")
        await tts(text, path=audiobook, to_lang="es")
        await sleep(2)
        if VOICE_CHATS.get(message.chat.id) is None:
            await msg.edit("\U0001fa84 **__Joining the voice chat...__**")
            await on_call.join(message.chat.id)
            VOICE_CHATS[message.chat.id] = on_call
        await sleep(2)
        await on_call.start_audio(audiobook, repeat=False)
        await msg.edit("**__Started audiobook__**")
    except Exception as e:
        logging.error(e)
        await msg.edit(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
        if message.chat.id in VOICE_CHATS:
            await VOICE_CHATS[message.chat.id].stop()
            await clear_queue(message.chat)
            VOICE_CHATS.pop(message.chat.id)
        os.remove(book)
        os.remove(audiobook)
