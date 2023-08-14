import os
import re
import uuid
import logging
from asyncio import sleep
from pyrogram import filters, Client
from pyrogram.types import Message

# from bot.helpers.pkl import load_pkl
from bot.helpers.queues import get_queue
from bot import assistant, kreacher, on_call
from youtubesearchpython import VideosSearch
from bot.dbs.instances import VOICE_CHATS
from bot.helpers.progress import progress
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.helpers.yt import ydl
from bot.helpers.queues import (
    add_to_queue,
    clear_queue,
)

fotoplay = "https://telegra.ph/file/b6402152be44d90836339.jpg"
ngantri = "https://telegra.ph/file/b6402152be44d90836339.jpg"
thumb = "https://telegra.ph/file/3e14128ad5c9ec47801bd.jpg"

current_dir = os.path.dirname(os.path.abspath(__file__))

queues = os.path.join(current_dir, "../dbs/queues.pkl")


@kreacher.on_message(filters.regex(pattern="^[!?/]play_video"))
async def _(client: Client, message: Message):
    # QUEUE = await load_pkl(queues, "rb", "dict")
    try:
        msg = await message.reply("\u23F3 **__Processing...__**")
        await sleep(2)
        download_as = os.path.join(
            current_dir, f"../downloads/videos/{str(uuid.uuid4())}.mp4"
        )
        if not message.reply_to_message and not " " in message.text:
            return await msg.edit(
                "❗ __Master, try with an: \n\nLive stream link.\n\nYouTube video link.\n\nReply to an video to start video streaming!__",
            )

        elif " " in message.text:
            url = message.text.split(" ", 1)[1]
            if not "http" in url:
                return await msg.edit(
                    "❗ __Try with an:\n\nLive video stream link.\n\nYouTube video link.\n\nReply to an video to start video streaming!__",
                )
            regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
            match = re.match(regex, url)
            if VOICE_CHATS.get(message.chat.id) is None:
                await msg.edit("**__Joining the voice chat...__** \u23F3")
                await on_call.join(message.chat.id)
                VOICE_CHATS[message.chat.id] = on_call
                await sleep(2)
            if match:
                await msg.edit("🔄 **__Starting YouTube video stream...__**")
                meta = ydl.extract_info(url=url, download=False)
                formats = meta.get("formats", [meta])
                for f in formats:
                    ytstreamlink = f["url"]
                search = VideosSearch(ytstreamlink, limit=1)
                opp = search.result()["result"]
                oppp = opp[0]
                thumbid = oppp["thumbnails"][0]["url"]
                split = thumbid.split("?")
                thumb = split[0].strip()

            else:
                await msg.edit("🔄 **__Starting live video stream...__**")
                await sleep(2)
                await on_call.start_video(
                    url,
                    enable_experimental_lip_sync=True,
                    repeat=False,
                    with_audio=True,
                )
                # await msg.delete()
                await msg.edit(
                    "\U00002378 **Started video streaming!**",
                    # photo=thumb,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "\u23EA", callback_data="back"
                                ),
                                InlineKeyboardButton(
                                    "\u23F8\uFE0F",
                                    callback_data="pause_or_resume",
                                ),
                                InlineKeyboardButton(
                                    "\u23ED\uFE0F", callback_data="next"
                                ),
                            ],
                        ],
                    ),
                )
        elif message.reply_to_message.video or message.reply_to_message.file:
            await msg.edit("🔄 **__Downloading...__**")
            media = await assistant.download_media(
                message.reply_to_message.video,
                file_name=download_as,
                progress=progress,
                progress_args=(client, message.chat, msg)
            )
            if VOICE_CHATS.get(message.chat.id) is None:
                await msg.edit("**__Joining the voice chat...__** \u23F3")
                await on_call.join(message.chat.id)
                VOICE_CHATS[message.chat.id] = on_call
                await sleep(2)
            await on_call.start_video(media, with_audio=True, repeat=False)
            # await msg.delete()
            await msg.edit(
                "**Started video streaming!**",
                # photo=thumb,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "\u23EA", callback_data="back"
                            ),
                            InlineKeyboardButton(
                                "\u23F8\uFE0F",
                                callback_data="pause_or_resume",
                            ),
                            InlineKeyboardButton(
                                "\u23ED\uFE0F", callback_data="next"
                            ),
                        ],
                    ],
                ),
            )
    except Exception as e:
        logging.error(e)
        await msg.edit(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
        if message.chat.id in VOICE_CHATS:
            await VOICE_CHATS[message.chat.id].stop()
            await clear_queue(message.chat)
            VOICE_CHATS.pop(message.chat.id)


"""
@kreacher.on(events.NewMessage(pattern="^[!?/]playlist"))
async def playlist(message):
    QUEUE = await load_pkl(queues, "rb", "dict")
    chat = message.chat
    user = message.get_sender()
    if not user.is_admin:
        await message.reply(
            "Sorry, you must be an administrator to execute this command."
        )
        return
    if chat.id in QUEUE:
        chat_queue = get_queue(chat)
        if len(chat_queue) == 1:
            await message.reply(
                f"**�PlAYLIST:**\n• [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                link_preview=False,
            )
        else:
            PLAYLIST = f"**🎧 PLAYLIST:**\n**• [{chat_queue[0][0]}]({chat_queue[0][2]})** | `{chat_queue[0][3]}` \n\n**• Upcoming Streaming:**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                PLAYLIST = (
                    PLAYLIST + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`"
                )
            await message.reply(PLAYLIST, link_preview=False)
    else:
        await message.reply("**Ntg is Streaming**")


@kreacher.on(events.NewMessage(pattern="^[!?/]pause"))
async def pause(message):
    QUEUE = await load_pkl(queues, "rb", "dict")
    chat = message.chat
    user = message.get_sender()
    if not user.is_admin:
        await message.reply(
            "Sorry, you must be an administrator to execute this command."
        )
        return
    if chat.id in QUEUE:
        try:
            await VOICE_CHATS[chat.id].pause_stream(chat.id)
            await message.reply("**Streaming Paused**")
        except Exception as e:
            await message.reply(f"**ERROR:** `{e}`")
    else:
        await message.reply("**Nothing Is Playing**")


@kreacher.on(events.NewMessage(pattern="^[!?/]resume"))
async def resume(message):
    QUEUE = await load_pkl(queues, "rb", "dict")
    chat = message.chat
    user = message.get_sender()
    if not user.is_admin:
        await message.reply(
            "Sorry, you must be an administrator to execute this command."
        )
        return
    if chat.id in QUEUE:
        try:
            await VOICE_CHATS[chat.id].resume_stream(chat.id)
            await message.reply("**Streaming Started Back 🔙**")
        except Exception as e:
            await message.reply(f"**ERROR:** `{e}`")
    else:
        await message.reply("**Nothing Is Streaming**")
"""
