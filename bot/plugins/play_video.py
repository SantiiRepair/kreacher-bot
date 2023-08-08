import os
import re
import uuid
import pickle
from asyncio import sleep
from youtubesearchpython import VideosSearch
from bot import client, kreacher, on_call
from bot.helpers.queues import get_queue
from bot.helpers.pkl import load_pkl
from bot.instance_of.every_vc import VOICE_CHATS
from pyrogram import Button, filters
from bot.helpers.progress import progress_callback
from yt_dlp import YoutubeDL

fotoplay = "https://telegra.ph/file/b6402152be44d90836339.jpg"
ngantri = "https://telegra.ph/file/b6402152be44d90836339.jpg"
thumb = "https://telegra.ph/file/3e14128ad5c9ec47801bd.jpg"

dir = os.path.dirname(os.path.abspath(__file__))

queues = os.path.join(dir, "../dbs/queues.pkl")

ydl = YoutubeDL(
    {
        "quiet": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
    }
)


@kreacher.on_message(filters.regex(pattern="^[!?/]play_video"))
async def play_video(client, message):
    QUEUE = load_pkl(queues, "rb", "dict")
    chat = message.chat
    replied = await message.get_reply_message()
    msg = await message.reply("🔄 **__Processing...__**")
    await sleep(2)
    download_as = os.path.join(dir, f"../downloads/videos/{str(uuid.uuid4())}")
    if not replied and not " " in message.message.message:
        await msg.edit(
            "❗ __Master, try with an: \n\nLive stream link.\n\nYouTube video link.\n\nReply to an video to start video streaming!__",
        )

    elif " " in message.message.message:
        text = message.message.message.split(" ", 1)
        url = text[1]
        if not "http" in url:
            return await msg.edit(
                "❗ __Try with an:\n\nLive video stream link.\n\nYouTube video link.\n\nReply to an video to start video streaming!__",
            )
        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, url)
        if VOICE_CHATS.get(chat.id) is None:
            try:
                await msg.edit("**__Joining the voice chat...__**")
                await on_call.join(chat.id)
                VOICE_CHATS[chat.id] = on_call
                await sleep(2)
            except Exception as e:
                await msg.edit(
                    f"__Oops master, something wrong has happened.__ \n\n`Error: {e}`",
                )
                await VOICE_CHATS[chat.id].stop()
                VOICE_CHATS.pop(chat.id)
                return await sleep(2)
        if match:
            await msg.edit("🔄 **__Starting YouTube video stream...__**")
            try:
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
            except Exception as e:
                await msg.edit(
                    f"❌ __Master, YouTube download error!__ \n\n`Error: {e}`",
                )
                print(e)
                await VOICE_CHATS[chat.id].stop()
                VOICE_CHATS.pop(chat.id)
                return await sleep(2)

        else:
            await msg.edit("🔄 **__Starting live video stream...__**")

        try:
            await sleep(2)
            await on_call.start_video(url, with_audio=True, repeat=False)
            await msg.delete()
            await msg.edit(
                "\U00002378 **Started video streaming!**",
                file=thumb,
                reply_markup=[
                    [
                        InlineKeyboardButton("\u23EA", data="back_callback"),
                        InlineKeyboardButton(
                            "\u23F8\uFE0F", data="pause_or_resume_callback"
                        ),
                        InlineKeyboardButton(
                            "\u23ED\uFE0F", data="next_callback"
                        ),
                    ],
                    [InlineKeyboardButton("cʟᴏꜱᴇ", data="end_callback")],
                ],
            )
        except Exception as e:
            await msg.edit(
                f"❌ **An error occoured!** \n\n`Error: {e}`",
            )
            await VOICE_CHATS[chat.id].stop()
            VOICE_CHATS.pop(chat.id)
            return await sleep(2)

    elif replied.video or replied.file:
        await msg.edit("🔄 **__Downloading...__**")
        media = await replied.download_media(
            file=download_as,
            progress_callback=progress_callback,
        )

        try:
            await sleep(2)
            await on_call.start_video(media, with_audio=True, repeat=False)
            await msg.delete()
            await message.reply(
                "**Started video streaming!**",
                file=thumb,
                reply_markup=[
                    [
                        InlineKeyboardButton("\u23EA", data="back_callback"),
                        InlineKeyboardButton(
                            "\u23F8\uFE0F", data="pause_or_resume_callback"
                        ),
                        InlineKeyboardButton(
                            "\u23ED\uFE0F", data="next_callback"
                        ),
                    ],
                    [InlineKeyboardButton("cʟᴏꜱᴇ", data="end_callback")],
                ],
            )
        except Exception as e:
            await msg.edit(
                f"❌ **An error occoured!** \n\n`Error: {e}`",
            )
            print(e)
            await VOICE_CHATS[chat.id].stop()
            VOICE_CHATS.pop(chat.id)
            return await sleep(2)

    else:
        await msg.edit(
            "__\U0001F9D9 Do you want to search for a YouTube video?__"
        )
        return await sleep(2)


@kreacher.on(events.NewMessage(pattern="^[!?/]playlist"))
async def playlist(message):
    QUEUE = load_pkl(queues, "rb", "dict")
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
    QUEUE = load_pkl(queues, "rb", "dict")
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
    QUEUE = load_pkl(queues, "rb", "dict")
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
