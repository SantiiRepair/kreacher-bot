from kreacher.helpers.thumbnail import gen_thumb
from Config import Config
from telethon import Button, events
from kreacher.dicts.dicts import VOICE_CHATS
from kreacher.helpers.queues import (
    QUEUE,
    add_to_queue,
    clear_queue,
    get_queue,
    pop_an_item,
    active,
)
from kreacher.helpers.yt_dlp import bash
from kreacher import ins, kreacher
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from pytgcalls.exceptions import (
    NoActiveGroupCall,
    NotInGroupCallError
)
from kreacher.status import g
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


async def skip_item(chat_id: int, x: int):
    if chat_id not in QUEUE:
        return 0
    chat_queue = get_queue(chat_id)
    try:
        songname = chat_queue[x][0]
        chat_queue.pop(x)
        return songname
    except Exception as e:
        print(e)
        return 0


async def skip_current_song(chat):
    if chat.id not in QUEUE:
        return 0
    chat_queue = get_queue(chat.id)
    if len(chat_queue) == 1:
        await VOICE_CHATS[chat.id].leave_group_call(chat.id)
        clear_queue(chat.id)
        active.remove(chat.id)
        return 1
    songname = chat_queue[1][0]
    url = chat_queue[1][1]
    link = chat_queue[1][2]
    type = chat_queue[1][3]
    RESOLUSI = chat_queue[1][4]
    if type == "Audio":
        await VOICE_CHATS[chat.id].change_stream(
            chat.id,
            AudioPiped(
                url,
            ),
        )
    elif type == "Video":
        if RESOLUSI == 720:
            hm = HighQualityVideo()
        elif RESOLUSI == 480:
            hm = MediumQualityVideo()
        elif RESOLUSI == 360:
            hm = LowQualityVideo()
        await VOICE_CHATS[chat.id].change_stream(
            chat.id, AudioVideoPiped(url, HighQualityAudio(), hm)
        )
    pop_an_item(chat.id)
    return [songname, link, type]


@kreacher.on(events.NewMessage(pattern="^[?!/]play_song"))
async def play_song(event):
    title = ' '.join(event.text[5:])
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
        return await event.client.send_file(chat.id, Config.CMD_IMG, caption="**Give Me Your Query Which You want to Play**\n\n **Example**: `/play Nira Ishq Bass boosted`", buttons=[[Button.inline("cʟᴏꜱᴇ", data="cls")]])
    elif replied and not replied.audio and not replied.voice or not replied:
        botman = await event.reply("🔎")
        query = event.text.split(maxsplit=1)[1]
        search = ytsearch(query)
        if search == 0:
            await botman.edit(
                "**Can't Find Song** Try searching with More Specific Title"
            )
        else:
            songname = search[0]
            title = search[0]
            url = search[1]
            duration = search[2]
            videoid = search[4]
            thumb = await gen_thumb(videoid)
            format = "best[height<=?720][width<=?1280]"
            hm, ytlink = await ytdl(format, url)
            if hm == 0:
                await botman.edit(f"`{ytlink}`")
            elif chat.id in QUEUE:
                pos = add_to_queue(chat.id, songname, ytlink, url, "Audio", 0)
                caption = f"✨ **ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ ᴀᴛ** {pos}\n\n❄ **ᴛɪᴛʟᴇ :** [{songname}]({url})\n⏱ **ᴅᴜʀᴀᴛɪᴏɴ :** {duration} ᴍɪɴᴜᴛᴇs\n🥀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {from_user}"
                await botman.delete()
                await event.client.send_file(chat.id, thumb, caption=caption, buttons=[[Button.inline("cʟᴏꜱᴇ", data="cls")]])
            else:
                try:
                    await ins.join(
                        chat.id,
                        AudioPiped(
                            ytlink,
                        ),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat.id, songname, ytlink, url, "Audio", 0)
                    caption = f"➻ **sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ**\n\n🌸 **ᴛɪᴛʟᴇ :** [{songname}]({url})\n⏱ **ᴅᴜʀᴀᴛɪᴏɴ :** {duration} ᴍɪɴᴜᴛᴇs\n🥀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {from_user}"
                    await botman.delete()
                    await event.client.send_file(chat.id, thumb, caption=caption, buttons=[[Button.inline("cʟᴏꜱᴇ", data="cls")]])
                except Exception as ep:
                    clear_queue(chat.id)
                    await botman.edit(f"`{ep}`")

    else:
        botman = await event.edit("➕ Downloading File...")
        dl = await replied.download_media()
        link = f"https://t.me/c/{chat.id}/{event.reply_to_msg_id}"
        if replied.audio:
            songname = "Telegram Music Player"
        elif replied.voice:
            songname = "Voice Note"
        if chat.id in QUEUE:
            pos = add_to_queue(chat.id, songname, dl, link, "Audio", 0)
            caption = f"✨ **ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ ᴀᴛ** {pos}\n\n❄ **ᴛɪᴛʟᴇ :** [{songname}]({url})\n🥀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {from_user}"
            await event.client.send_file(chat.id, ngantri, caption=caption, buttons=[[Button.inline("cʟᴏꜱᴇ", data="cls")]])
            await botman.delete()
        else:
            try:
                await ins.join(
                    chat.id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat.id, songname, dl, link, "Audio", 0)
                caption = f"➻ **sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ**\n\n🌸 **ᴛɪᴛʟᴇ :** [{songname}]({link})\n🥀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {from_user}"
                await event.client.send_file(chat.id, fotoplay, caption=caption, buttons=[[Button.inline("cʟᴏꜱᴇ", data="cls")]])
                await botman.delete()
            except Exception as ep:
                clear_queue(chat.id)
                await botman.edit(f"`{ep}`")
