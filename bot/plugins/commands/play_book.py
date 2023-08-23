import os
import uuid
import PyPDF2
import logging
from asyncio import sleep
from bot.helpers.tts import tts
from bot import kreacher, on_call
from pyrogram.types import Message
from html.parser import HTMLParser
from pyrogram import filters, Client
from bot.helpers.progress import progress
from bot.dbs.instances import VOICE_CHATS
from bot.decorators.only_grps_chnns import only_grps_chnns
from ebooklib import epub as epublib, ITEM_IMAGE, ITEM_DOCUMENT
from bot.helpers.queues import (
    clear_queue,
)

c = os.path.dirname(os.path.abspath(__file__))


@kreacher.on_message(filters.regex(pattern="^[!?/]play_book"))
@only_grps_chnns
async def _(client: Client, message: Message):
    text = ""
    h = _HTMLFilter()
    book = os.path.join(c, f"../../downloads/books/{str(uuid.uuid4())}.pdf")
    audiobook = os.path.join(
        c, f"../../downloads/audiobooks/{str(uuid.uuid4())}.wav"
    )
    try:
        if not message.reply_to_message:
            return await message.reply(
                "**__How to use this command.\n\nNext we show two ways to use this command, click on the button with the mode you are looking for to know details.__**"
            )
        msg = await message.reply("\u23F3 **__Processing...__**")
        await sleep(2)
        file_type = message.reply_to_message.document.mime_type.split("/", 1)[
            1
        ]
        book = os.path.join(
            c, f"../../downloads/books/{str(uuid.uuid4())}.{file_type}"
        )

        await msg.edit("\U0001f4be **__Downloading...__**")
        f = await message.reply_to_message.download(
            file_name=book,
            progress=progress,
            progress_args=(client, message.chat, msg),
        )

        if " " not in message.text and file_type == "pdf":
            pdf = PyPDF2.PdfReader(open(f, "rb"))
            await msg.edit("**__Grouping pages...__**")
            for pgs in range(len(pdf.pages)):
                text += pdf.pages[pgs].extract_text()
            await msg.edit(f"**__{len(pdf.pages)} pages were grouped__**")
        elif " " not in message.text and "epub" in file_type:
            epub_pages = 0
            epub = epublib.read_epub(f)
            await msg.edit("**__Grouping pages...__**")
            for item in epub.get_items():
                if item.get_type() == ITEM_DOCUMENT:
                    h.feed(item.get_body_content().decode())
                    text += h.text
                    epub_pages += 1
            await msg.edit(f"**__{epub_pages} pages were grouped__**")
        elif " " in message.text and file_type == "pdf":
            pdf = PyPDF2.PdfReader(open(f, "rb"))
            page_number = message.text.split(maxsplit=1)[1]
            if not page_number.isdigit():
                return await msg.edit("**__This is not a number__**")
            text += pdf.pages[int(page_number)].extract_text()
        elif " " in message.text and "epub" in file_type:
            epub = epublib.read_epub(f)
            page_number = message.text.split(maxsplit=1)[1]
            if not page_number.isdigit():
                return await msg.edit("**__This is not a number__**")
            # h.feed(epub.get_items().get_body_content().decode())
            # text += h.text
            # text += epub.get_items_of_type(ITEM_DOCUMENT)
        await sleep(2)
        await msg.edit("**__Generating an audiobook__**")
        await tts(text=text, output_file=audiobook)
        await sleep(2)
        if VOICE_CHATS.get(message.chat.id) is None:
            await msg.edit("\U0001fa84 **__Joining the voice chat...__**")
            await on_call.join(message.chat.id)
            VOICE_CHATS[message.chat.id] = on_call
        await sleep(2)
        await on_call.start_audio(audiobook, repeat=False)
        if "epub" in file_type:
            epub = epublib.read_epub(f)
            for image in epub.get_items_of_type(ITEM_IMAGE):
                print(image)
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


class _HTMLFilter(HTMLParser):
    text = ""

    def handle_data(self, data):
        self.text += data
