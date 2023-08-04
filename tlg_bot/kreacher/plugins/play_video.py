import re
from youtubesearchpython import VideosSearch
from kreacher import kreacher
from kreacher.helpers.queues import QUEUE, get_queue
from kreacher.helpers.voice_chats import create_voice_chat, get_voice_chat, stop_voice_chat
from telethon import Button, events
from asyncio import sleep
from yt_dlp import YoutubeDL as ydl
fotoplay = "https://telegra.ph/file/b6402152be44d90836339.jpg"
ngantri = "https://telegra.ph/file/b6402152be44d90836339.jpg"


@kreacher.on(events.callbackquery.CallbackQuery(data="cls"))
async def _(event):
    await event.delete()


@kreacher.on(events.callbackquery.CallbackQuery(data="pause_callback"))
async def _(event):
    chat = await event.get_chat()
    call_py = await get_voice_chat(chat.id)
    await call_py.set_pause(True)


@kreacher.on(events.callbackquery.CallbackQuery(data="resume_callback"))
async def _(event):
    chat = await event.get_chat()
    call_py = await get_voice_chat(chat.id)
    await call_py.set_pause(False)


@kreacher.on(events.callbackquery.CallbackQuery(data="end_callback"))
async def _(event):
    chat = await event.get_chat()
    call_py = await get_voice_chat(chat.id)
    await call_py.stop_media()


@kreacher.on(events.NewMessage(pattern="^[?!/]play_video"))
async def play_video(event):
    chat = await event.get_chat()
    call_py = await get_voice_chat(chat.id)
    msg = await event.reply("🔄 <i>Processing...</i>", parse_mode="HTML")
    media = await event.get_reply_message()
    if not media and not ' ' in event.message.message:
        await msg.edit("❗ __Send Me An Live Stream Link / YouTube Video Link / Reply To An Video To Start Video Streaming!__")

    elif ' ' in event.message.message:
        text = event.message.message.split(' ', 1)
        url = text[1]
        if not 'http' in url:
            return await msg.edit("❗ __Send Me An Live Stream Link / YouTube Video Link / Reply To An Video To Start Video Streaming!__")
        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, url)
        if call_py is None:
            await msg.edit("<i>Joining the voice chat...</i>", parse_mode="HTML")
            await create_voice_chat(chat.id)
        if match:
            await msg.edit("🔄 <i>Starting YouTube Video Stream...</i>", parse_mode="HTML")
            try:
                meta = ydl().extract_info(url=url, download=False)
                formats = meta.get('formats', [meta])
                for f in formats:
                    ytstreamlink = f['url']
                link = ytstreamlink
                search = VideosSearch(url, limit=1)
                opp = search.result()["result"]
                oppp = opp[0]
                thumbid = oppp["thumbnails"][0]["url"]
                split = thumbid.split("?")
                thumb = split[0].strip()
            except Exception as e:
                await msg.edit(f"❌ **YouTube Download Error !** \n\n`{e}`")
                print(e)
                await stop_voice_chat(chat.id)
                return await call_py.stop()

        else:
            await msg.edit("🔄 `Starting Live Video Stream ...`")
            link = url
            thumb = "https://telegra.ph/file/3e14128ad5c9ec47801bd.jpg"

        try:
            await sleep(2)
            await call_py.start_video(link, with_audio=True, repeat=False)
            await msg.delete()
            await event.reply(
                f"▶️ **Started [Video Streaming]({url})!**",
                file=thumb,
                buttons=[
                    [Button.inline("⏸", data="pause_callback"),
                     Button.inline("▶️", data="resume_callback")],
                    [Button.inline("⏹️", data="end_callback")],
                ],
            )
        except Exception as e:
            await msg.edit(f"❌ **An Error Occoured !** \n\nError: `{e}`")
            await stop_voice_chat(chat.id)
            return await call_py.stop()

    elif media.video or media.file:
        await msg.edit("🔄 `Downloading ...`")
        if media.video and media.video.thumbs:
            lol = media.video.thumbs[0]
            lel = await kreacher.download_media(lol['file_id'])
            thumb = lel
        else:
            thumb = "https://telegra.ph/file/62e86d8aadde9a8cbf9c2.jpg"

        video = await kreacher.download_media(media)

        try:
            await sleep(2)
            await call_py.start_video(video, with_audio=True, repeat=False)
            await msg.delete()
            await event.reply(
                f"▶️ **Started [Video Streaming](https://t.me/AsmSafone)!**",
                file=thumb,
                buttons=[
                    [Button.inline("⏸", data="pause_callback"),
                     Button.inline("▶️", data="resume_callback")],
                    [Button.inline("⏹️", data="end_callback")],
                ]
            )
        except Exception as e:
            await msg.edit(f"❌ **An Error Occoured !** \n\nError: `{e}`")
            print(e)
            await stop_voice_chat(chat.id)
            return await call_py.stop()

    else:
        await msg.edit("💁🏻‍♂️ Do you want to search for a YouTube video?")


@kreacher.on(events.NewMessage(pattern="^[?!/]playlist"))
async def playlist(event, perm):
    chat_id = event.chat_id
    user = event.get_sender()
    if not user.is_admin:
        await event.reply(
            "Sorry, you must be an administrator to execute this command."
        )
        return
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
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


@kreacher.on(events.NewMessage(pattern="^[?!/]pause"))
async def pause(event, perm):
    chat_id = event.chat_id
    user = event.get_sender()
    if not user.is_admin:
        await event.reply(
            "Sorry, you must be an administrator to execute this command."
        )
        return
    if chat_id in QUEUE:
        try:
            #await call_py.pause_stream(chat_id)
            await event.reply("**Streaming Paused**")
        except Exception as e:
            await event.reply(f"**ERROR:** `{e}`")
    else:
        await event.reply("**Nothing Is Playing**")


@kreacher.on(events.NewMessage(pattern="^[?!/]resume"))
async def vc_resume(event, perm):
    chat_id = event.chat_id
    user = event.get_sender()
    if not user.is_admin:
        await event.reply(
            "Sorry, you must be an administrator to execute this command."
        )
        return
    if chat_id in QUEUE:
        try:
            #await call_py.resume_stream(chat_id)
            await event.reply("**Streaming Started Back 🔙**")
        except Exception as e:
            await event.reply(f"**ERROR:** `{e}`")
    else:
        await event.reply("**Nothing Is Streaming**")
