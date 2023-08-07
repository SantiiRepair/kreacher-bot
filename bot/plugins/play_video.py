import os
import re
import uuid
from asyncio import sleep
from youtubesearchpython import VideosSearch
from bot import client, ins, kreacher
from bot.helpers.queues import get_queue
from bot.dicts.dicts import QUEUE, VOICE_CHATS
from telethon import Button, events

from yt_dlp import YoutubeDL

fotoplay = "https://telegra.ph/file/b6402152be44d90836339.jpg"
ngantri = "https://telegra.ph/file/b6402152be44d90836339.jpg"
thumb = "https://telegra.ph/file/3e14128ad5c9ec47801bd.jpg"

ydl_opts = {
    "quiet": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
}
ydl = YoutubeDL(ydl_opts)


@kreacher.on(events.NewMessage(pattern="^[!?/]play_video"))
async def play_video(event):
    chat = await event.get_chat()
    media = await event.get_reply_message()
    msg = await event.reply("🔄 **__Processing...__**")
    await sleep(2)
    dir = os.path.dirname(os.path.abspath(__file__))
    download_as = os.path.join(dir, f"../downloads/videos/{str(uuid.uuid4())}")
    if not media and not " " in event.message.message:
        await msg.edit(
            "❗ __Master, try with an: \n\nLive stream link.\n\nYouTube video link.\n\nReply to an video to start video streaming!__",
        )

    elif " " in event.message.message:
        text = event.message.message.split(" ", 1)
        url = text[1]
        if not "http" in url:
            return await msg.edit(
                "❗ __Try with an:\n\nLive video stream link.\n\nYouTube video link.\n\nReply to an video to start video streaming!__",
            )
        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, url)
        if VOICE_CHATS.get(chat.id) is None:
            try:
                await msg.edit("__Joining the voice chat...__")
                await ins.join(chat.id)
                VOICE_CHATS[chat.id] = ins
                await sleep(3)
            except Exception as e:
                await msg.edit(
                    f"__Oops master, something wrong has happened. \n\nError:__ `{e}`",
                )
                await VOICE_CHATS[chat.id].stop()
                VOICE_CHATS.pop(chat.id)
                return await sleep(3)
        if match:
            await msg.edit("🔄 __Starting YouTube video stream...__")
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
                    f"❌ __Master, YouTube download error!</i> \n\n`Error: {e}`",
                )
                print(e)
                await VOICE_CHATS[chat.id].stop()
                VOICE_CHATS.pop(chat.id)
                return await sleep(3)

        else:
            await msg.edit("🔄 __Starting live video stream...__")

        try:
            await sleep(2)
            await ins.start_video(url, with_audio=True, repeat=False)
            await msg.delete()
            await msg.edit(
                "\U00002378 __Started video streaming!__",
                file=thumb,
                buttons=[
                    [
                        Button.inline("\u23EA", data="back_callback"),
                        Button.inline(
                            "\u23F8\uFE0F", data="pause_or_resume_callback"
                        ),
                        Button.inline("\u23ED\uFE0F", data="next_callback"),
                    ],
                    [Button.inline("cʟᴏꜱᴇ", data="cls")],
                ],
            )
        except Exception as e:
            await msg.edit(
                f"❌ **An error occoured!** \n\n`Error: {e}`",
            )
            await VOICE_CHATS[chat.id].stop()
            VOICE_CHATS.pop(chat.id)
            return await sleep(3)

    elif media.video or media.file:
        await msg.edit("🔄 __Downloading...__")
        video = await client.download_media(media, file=download_as)

        try:
            await sleep(2)
            await ins.start_video(video, with_audio=True, repeat=False)
            await msg.delete()
            await event.reply(
                "▶️ __Started video streaming!__",
                file=thumb,
                buttons=[
                    [
                        Button.inline("\u23EA", data="back_callback"),
                        Button.inline(
                            "\u23F8\uFE0F", data="pause_or_resume_callback"
                        ),
                        Button.inline("\u23ED\uFE0F", data="next_callback"),
                    ],
                    [Button.inline("cʟᴏꜱᴇ", data="cls")],
                ],
            )
        except Exception as e:
            await msg.edit(
                f"❌ **An error occoured!** \n\n`Error: {e}`",
            )
            print(e)
            await VOICE_CHATS[chat.id].stop()
            VOICE_CHATS.pop(chat.id)
            return await sleep(3)

    else:
        await msg.edit(
            "__\U0001F9D9 Do you want to search for a YouTube video?__"
        )
        return await sleep(3)


@kreacher.on(events.NewMessage(pattern="^[!?/]playlist"))
async def playlist(event):
    chat = event.get_chat()
    user = event.get_sender()
    if not user.is_admin:
        await event.reply(
            "Sorry, you must be an administrator to execute this command."
        )
        return
    if chat.id in QUEUE:
        chat_queue = get_queue(chat)
        if len(chat_queue) == 1:
            await event.reply(
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
            await event.reply(PLAYLIST, link_preview=False)
    else:
        await event.reply("**Ntg is Streaming**")


@kreacher.on(events.NewMessage(pattern="^[!?/]pause"))
async def pause(event):
    chat = event.get_chat()
    user = event.get_sender()
    if not user.is_admin:
        await event.reply(
            "Sorry, you must be an administrator to execute this command."
        )
        return
    if chat.id in QUEUE:
        try:
            await VOICE_CHATS[chat.id].pause_stream(chat.id)
            await event.reply("**Streaming Paused**")
        except Exception as e:
            await event.reply(f"**ERROR:** `{e}`")
    else:
        await event.reply("**Nothing Is Playing**")


@kreacher.on(events.NewMessage(pattern="^[!?/]resume"))
async def resume(event):
    chat = event.get_chat()
    user = event.get_sender()
    if not user.is_admin:
        await event.reply(
            "Sorry, you must be an administrator to execute this command."
        )
        return
    if chat.id in QUEUE:
        try:
            await VOICE_CHATS[chat.id].resume_stream(chat.id)
            await event.reply("**Streaming Started Back 🔙**")
        except Exception as e:
            await event.reply(f"**ERROR:** `{e}`")
    else:
        await event.reply("**Nothing Is Streaming**")
