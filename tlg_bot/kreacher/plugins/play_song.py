from asyncio import sleep
from kreacher.helpers.thumbnail import gen_thumb
from telethon import Button, events
from kreacher.dicts.dicts import QUEUE, VOICE_CHATS
from kreacher.helpers.queues import (
    add_to_queue,
    clear_queue,
    get_queue,
)
from kreacher.helpers.yt_dlp import bash
from kreacher import config, ins, kreacher
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


@kreacher.on(events.NewMessage(pattern="[!?/]play_song"))
async def play_song(event):
    title = " ".join(event.text[5:])
    replied = await event.get_reply_message()
    chat = await event.get_chat()
    from_user = vcmention(event.sender)
    if (
        replied
        and not replied.audio
        and not replied.voice
        and not title
        or not replied
        and not title
    ):
        return await event.client.send_file(
            chat.id,
            config.CMD_IMG,
            caption="**Give Me Your Query Which You want to Play**\n\n **Example**: `/play Nira Ishq Bass boosted`",
            buttons=[[Button.inline("cʟᴏꜱᴇ", data="cls")]],
        )
    elif replied and not replied.audio and not replied.voice or not replied:
        msg = await event.reply("🔎")
        query = event.text.split(maxsplit=1)[1]
        search = ytsearch(query)
        if search == 0:
            await msg.edit(
                "**Can't Find Song** Try searching with More Specific Title"
            )
        else:
            name = search[0]
            title = search[0]
            ref = search[1]
            duration = search[2]
            videoid = search[4]
            thumb = await gen_thumb(videoid)
            format = "best[height<=?720][width<=?1280]"
            hm, url = await ytdl(format, ref)
            if hm == 0:
                await msg.edit(f"`{url}`")
            elif chat.id in QUEUE:
                pos = add_to_queue(chat, name, url, ref, "audio")
                caption = f"✨ **ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ ᴀᴛ** {pos}\n\n❄ **ᴛɪᴛʟᴇ :** [{name}]({url})\n⏱ **ᴅᴜʀᴀᴛɪᴏɴ :** {duration} ᴍɪɴᴜᴛᴇs\n🥀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {from_user}"
                await msg.delete()
                await event.client.send_file(
                    chat.id,
                    thumb,
                    caption=caption,
                    buttons=[[Button.inline("cʟᴏꜱᴇ", data="cls")]],
                )
            else:
                try:
                    await ins.join(chat.id)
                    await ins.start_audio(url, repeat=False)
                    VOICE_CHATS[chat.id] = ins
                    add_to_queue(chat, name, url, ref, "audio")
                    caption = f"➻ **sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ**\n\n🌸 **ᴛɪᴛʟᴇ :** [{name}]({url})\n⏱ **ᴅᴜʀᴀᴛɪᴏɴ :** {duration} ᴍɪɴᴜᴛᴇs\n🥀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {from_user}"
                    await msg.delete()
                    await event.client.send_file(
                        chat.id,
                        thumb,
                        caption=caption,
                        buttons=[[Button.inline("cʟᴏꜱᴇ", data="cls")]],
                    )
                except Exception as ep:
                    clear_queue(chat)
                    VOICE_CHATS.pop(chat.id)
                    await msg.edit(f"`{ep}`")
                    return await sleep(3)

    else:
        msg = await event.edit("➕ Downloading File...")
        dl = await replied.download_media()
        link = f"https://t.me/c/{chat.id}/{event.reply_to_msg_id}"
        if replied.audio:
            name = "Audio File"
        elif replied.voice:
            name = "Voice Note"
        if chat.id in QUEUE:
            pos = add_to_queue(chat, name, url, ref, "audio")
            caption = f"✨ **ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ ᴀᴛ** {pos}\n\n❄ **ᴛɪᴛʟᴇ :** [{name}]({url})\n🥀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {from_user}"
            await event.client.send_file(
                chat.id,
                ngantri,
                caption=caption,
                buttons=[[Button.inline("cʟᴏꜱᴇ", data="cls")]],
            )
            await msg.delete()
        else:
            try:
                await ins.join(chat.id)
                await ins.start_audio(dl, repeat=False)
                VOICE_CHATS[chat.id] = ins
                add_to_queue(chat, name, url, ref, "audio")
                caption = f"<b>Started Streaming</b>\n\n <b>Title: </b> [{name}]({link})\n <b>Requested by: </b> {from_user}"
                await event.client.send_file(
                    chat.id,
                    fotoplay,
                    caption=caption,
                    buttons=[
                        [
                            Button.inline(
                                "\U000023ee ʙᴀᴄᴋ", data="back_callback"
                            ),
                            Button.inline(
                                "\U0001F501 ᴘᴀᴜsᴇ",
                                data="pause_or_resume_callback",
                            ),
                            Button.inline(
                                "\U000023ED ɴᴇxᴛ", data="next_callback"
                            ),
                        ],
                        [Button.inline("cʟᴏꜱᴇ", data="cls")],
                    ],
                    parse_mode="HTML",
                )
                await msg.delete()
            except Exception as e:
                clear_queue(chat)
                VOICE_CHATS.pop(chat.id)
                await msg.edit(f"`{e}`")
                return await sleep(3)
