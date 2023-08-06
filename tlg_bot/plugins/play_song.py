import os
import uuid
from asyncio import sleep

# from tlg_bot.helpers.thumbnail import gen_thumb
from telethon import Button, events
from tlg_bot.dicts.dicts import QUEUE, VOICE_CHATS
from tlg_bot.helpers.queues import (
    add_to_queue,
    clear_queue,
)
from tlg_bot.helpers.yt_dlp import bash
from tlg_bot import config, ins, kreacher
from telethon.tl import types
from telethon.utils import get_display_name
from youtubesearchpython import VideosSearch


fotoplay = "https://telegra.ph/file/b6402152be44d90836339.jpg"
ngantri = "https://telegra.ph/file/b6402152be44d90836339.jpg"
owner = "1669178360"


def vcmention(user):
    full_name = get_display_name(user)
    if not isinstance(user, types.User):
        return full_name
    return f"[{full_name}](tg://user?id={user.id})"


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        videoid = data["id"]
        return [songname, url, duration, thumbnail, videoid]
    except Exception as e:
        print(e)
        return 0


async def ytdl(format: str, link: str):
    stdout, stderr = await bash(f'yt-dlp -g -f "{format}" {link}')
    if stdout:
        return 1, stdout.split("\n")[0]
    return 0, stderr


@kreacher.on(events.NewMessage(pattern="^[!?/]play_song"))
async def play_song(event):
    title = " ".join(event.text[5:])
    replied = await event.get_reply_message()
    chat = await event.get_chat()
    msg = await event.reply("🔄 **__Processing...__**")
    await sleep(2)
    dir = os.path.dirname(os.path.abspath(__file__))
    downloads_dir = os.path.join(dir, "../downloads/songs/")
    from_user = vcmention(event.sender)
    if (
        replied
        and not replied.audio
        and not replied.voice
        and not title
        or not replied
        and not title
    ):
        return await msg.edit(
            "__Give me your query which you want to play\n\n Example:__ `/play Hey Boy Sia`",
            file=config.CMD_IMG,
            buttons=[[Button.inline("cʟᴏꜱᴇ", data="cls")]],
        )
    elif VOICE_CHATS.get(chat.id) is None:
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
    if replied and not replied.audio and not replied.voice or not replied:
        query = event.text.split(maxsplit=1)[1]
        search = ytsearch(query)
        if search == 0:
            await msg.edit(
                "__Can't find song.\n\nTry searching with more specific title.__",
            )
        else:
            name = search[0]
            title = search[0]
            ref = search[1]
            duration = search[2]
            videoid = search[4]
            # thumb = await gen_thumb(videoid)
            format = "best[height<=?720][width<=?1280]"
            hm, url = await ytdl(format, ref)
            if hm == 0:
                await msg.edit(f"`{url}`")
            elif chat.id in QUEUE:
                pos = add_to_queue(chat, name, url, ref, "audio")
                await msg.edit(
                    f"__Added to queue at {pos}\n\n Title: [{name}]({url})\nDuration: {duration} Minutes\n Requested by:__ {from_user}",
                    # file=thumb,
                    buttons=[[Button.inline("cʟᴏꜱᴇ", data="cls")]],
                )

                try:
                    await ins.start_audio(url, repeat=False)
                    add_to_queue(chat, name, url, ref, "audio")
                    await sleep(3)
                    await msg.edit(
                        f"**__Started Streaming__**\n\n **Title**: [{name}]({url})\n **Duration:** {duration} **Minutes\n Requested by:** {from_user}",
                        # file=thumb,
                        buttons=[
                            [
                                Button.inline("\u23EA", data="back_callback"),
                                Button.inline(
                                    "\u23F8\uFE0F",
                                    data="pause_or_resume_callback",
                                ),
                                Button.inline(
                                    "\u23ED\uFE0F", data="next_callback"
                                ),
                            ],
                            [Button.inline("cʟᴏꜱᴇ", data="cls")],
                        ],
                    )
                except Exception as e:
                    clear_queue(chat)
                    await VOICE_CHATS[chat.id].stop()
                    await msg.edit(f"`{e}`")
                    VOICE_CHATS.pop(chat.id)
                    return await sleep(3)

    else:
        await msg.edit("➕ __Downloading...__")
        dl = await replied.download_media(
            file=f"{downloads_dir} {str(uuid.uuid4())}"
        )
        link = f"https://t.me/c/{chat.id}/{event.reply_to_msg_id}"
        if replied.audio:
            name = "Audio File"
        elif replied.voice:
            name = "Voice Note"
        if chat.id in QUEUE:
            # pos = add_to_queue(chat, name, url, ref, "audio")
            await msg.edit(
                f"**__Added to queue at__** \n\n **Title:** [{name}]({url})\n **Requested by:** {from_user}",
                file=ngantri,
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
        else:
            try:
                await sleep(3)
                await ins.start_audio(dl, repeat=False)
                await msg.edit(
                    f"**__Started Streaming__**\n\n **Title:** [{name}]({link})\n **Requested by:** {from_user}",
                    file=fotoplay,
                    buttons=[
                        [
                            Button.inline("\u23EA", data="back_callback"),
                            Button.inline(
                                "\u23F8\uFE0F", data="pause_or_resume_callback"
                            ),
                            Button.inline(
                                "\u23ED\uFE0F", data="next_callback"
                            ),
                        ],
                        [Button.inline("cʟᴏꜱᴇ", data="cls")],
                    ],
                )
            except Exception as e:
                clear_queue(chat)
                await VOICE_CHATS[chat.id].stop()
                await msg.edit(f"`{e}`")
                VOICE_CHATS.pop(chat.id)
                return await sleep(3)
