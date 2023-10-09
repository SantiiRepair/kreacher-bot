import io
import os
import uuid
import PyPDF2
import shutup
import logging
from asyncio import sleep
from html.parser import HTMLParser
from pyrogram.types import Message
from pyrogram import filters, Client
from ebooklib import epub as epublib, ITEM_IMAGE, ITEM_DOCUMENT

from bot.helpers.tts import tts
from bot.helpers.progress import progress
from bot import kreacher, on_call, VOICE_CHATS
from bot.decorators.only_grps_chnns import only_grps_chnns
from bot.helpers.queues import (
    add_or_create_queue,
    get_queues,
    get_last_position_in_queue,
    remove_queue,
)

# used to hide ebooklib annoying warnings
shutup.please()
_cwd = os.path.dirname(os.path.abspath(__file__))


@kreacher.on_message(filters.regex(pattern="^[!?/]play_book"))
@only_grps_chnns
async def _(client: Client, message: Message):
    text = ""
    h = _HTMLFilter()
    try:
        if not message.reply_to_message:
            return await message.reply(
                "**__How to use this command.\n\nNext we show two ways to use this command, click on the button with the mode you are looking for to know details.__**"
            )
        msg = await message.reply("\u23F3 **__Processing...__**")
        await sleep(2)
        file_type = message.reply_to_message.document.mime_type.split("/", 1)[1]
        file_name = os.path.join(
            _cwd, f"../../downloads/books/{str(uuid.uuid4())}.{file_type}"
        )
        audiobook = os.path.join(_cwd, f"../../tmp/{str(uuid.uuid4())}.wav")
        await msg.edit("💾 **__Downloading...__**")
        f = await message.reply_to_message.download(
            file_name=file_name,
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
            epub = epublib.read_epub(f)
            await msg.edit("**__Grouping pages...__**")
            for i, item in enumerate(epub.get_items(), start=1):
                if item.get_type() == ITEM_DOCUMENT:
                    h.feed(item.get_body_content().decode())
                    text += h.text
            # pylint: disable=undefined-loop-variable
            await msg.edit(f"**__{i} pages were grouped__**")
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
                return await msg.edit("__This is not a number__")
            if "." in page_number:
                return await msg.edit("__Only integer numbers allowed__")
            for index, item in enumerate(epub.get_items(), start=1):
                if index == int(page_number) and item.get_type() == ITEM_DOCUMENT:
                    h.feed(item.get_body_content().decode())
                    text += h.text
        await sleep(2)
        await msg.edit("**__Generating an audiobook__**")
        await tts(text=text, output_file=audiobook)
        await sleep(2)
        if VOICE_CHATS.get(message.chat.id) is None:
            await msg.edit("🪄 **__Joining the voice chat...__**")
            await on_call.start(message.chat.id)
            VOICE_CHATS[message.chat.id] = on_call
        await sleep(2)
        await on_call.start_audio(audiobook, repeat=False)
        if "epub" in file_type:
            epub = epublib.read_epub(f)
            for item in epub.get_items_of_type(ITEM_IMAGE):
                photo = io.BytesIO(item.get_content())
                break
            await msg.delete()
            return await client.send_photo(
                message.chat.id,
                photo=photo,
                caption="**__Started audiobook__**",
            )
        await msg.edit("**__Started audiobook__**")
        if os.path.exists(file_name):
            os.remove(file_name)
    except Exception as e:
        logging.error(e)
        await msg.edit(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
        if message.chat.id in VOICE_CHATS:
            await VOICE_CHATS[message.chat.id].stop()
            remove_queue(str(message.chat.id))
            VOICE_CHATS.pop(message.chat.id)
        if os.path.exists(file_name):
            os.remove(file_name)
        elif os.path.exists(audiobook):
            os.remove(audiobook)


class _HTMLFilter(HTMLParser):
    text = ""

    def handle_data(self, data):
        self.text += data
