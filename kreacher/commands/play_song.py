import re
import uuid
import logging
from asyncio import sleep
from datetime import datetime
from pyrogram.types import Message
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.helpers.progress import progress
from bot.helpers.yt import ytsearch, ytdl
from bot.helpers.user_info import user_info
from bot import kreacher, tgcalls, VOICE_CHATS
from bot.decorators.sides import only_groups_or_channels
from bot.helpers.queues import (
    add_or_create_queue,
    get_queues,
    get_last_position_in_queue,
    remove_queue,
)

fotoplay = "https://telegra.ph/file/b6402152be44d90836339.jpg"
ngantri = "https://telegra.ph/file/b6402152be44d90836339.jpg"


@kreacher.on_message(filters.regex(pattern="^[!?/]play_song"))
@only_groups_or_channels
async def _(client: Client, message: Message):
    data = await user_info(message.from_user)
    if not message.reply_to_message and " " not in message.text:
        return await message.reply(
            "**__How to use this command.\n\nNext we show two ways to use this command, click on the button with the mode you are looking for to know details.__**",
        )

    _message = await message.reply("\u23F3 **__Processing...__**")
    await sleep(2)
    try:
        if " " in message.text:
            query = message.text.split(maxsplit=1)[1]
            if "http" in query:
                regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
                match = re.match(regex, query)
                if not match:
                    return await _message.edit(
                        "**__Sorry, but this doesn't seem to be a YouTube link__** \U0001f914"
                    )
            search = await ytsearch(query)
            name = search[0]
            ref = search[1]
            duration = search[2]
            fmt = "bestaudio/best"
            _, url = await ytdl(fmt, ref)
            if search == 0:
                return await _message.edit(
                    "**__Can't find song.\n\nTry searching with more specific title.__**",
                )
            if str(message.chat.id) in get_queues():
                position = get_last_position_in_queue(str(message.chat.id)) + 1
                add_or_create_queue(
                    str(message.chat.id),
                    from_user=str(message.from_user.id),
                    date=str(datetime.now()),
                    file=url,
                    type_of="song_yt",
                    position=position,
                )
                return await _message.edit(
                    f"**__Added to queue at {position}\n\nTitle: [{name}]({url})\nDuration: {duration} Minutes\n Requested by:__** [{data['first_name']}]({data['mention']})",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("cʟᴏꜱᴇ", callback_data="close")]]
                    ),
                )
            if str(message.chat.id) not in get_queues():
                add_or_create_queue(
                    str(message.chat.id),
                    from_user=str(message.from_user.id),
                    date=str(datetime.now()),
                    is_playing=True,
                    file=url,
                    type_of="song_yt",
                )
            if VOICE_CHATS.get(message.chat.id) is None:
                await _message.edit("🪄 **__Joining the voice chat...__**")
                VOICE_CHATS[message.chat.id] = tgcalls.get_group_call()
                await VOICE_CHATS[message.chat.id].start(message.chat.id)
            await sleep(2)
            await VOICE_CHATS[message.chat.id].start_audio(url, repeat=False)
            await _message.edit(
                f"**__Started Streaming__**\n\n **Title**: [{name}]({url})\n **Duration:** {duration} **Minutes\n Requested by:** [{data['first_name']}]({data['mention']})",
                # file=thumb,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("⏪", callback_data="back"),
                            InlineKeyboardButton(
                                "⏸️",
                                callback_data="pause_or_resume",
                            ),
                            InlineKeyboardButton(
                                "⏭️",
                                callback_data="next",
                            ),
                        ],
                    ]
                ),
            )
            return await _message.pin()
        if not message.reply_to_message.audio and not message.reply_to_message.voice:
            return await _message.edit(
                "**__Reply to an audio file or a voice note.__**",
            )
        file_name = (
            f"/tmp/{str(uuid.uuid4())}.{message.reply_to_message.audio.mime_type.split('/', 1)[1]}"
            if message.reply_to_message.audio
            else f"/tmp/{str(uuid.uuid4())}.mp3"
        )
        type_of = "Audio File" if message.reply_to_message.audio else "Voice Note"
        duration = (
            round((message.reply_to_message.audio.duration / 60), 2)
            if message.reply_to_message.audio
            else round((message.reply_to_message.voice.duration / 60), 2)
        )
        file = (
            f"https://t.me/c/{message.chat.id}/{message.reply_to_message.id}".replace(
                "/c/-100", "/c/"
            )
        )
        if str(message.chat.id) in get_queues():
            position = get_last_position_in_queue(str(message.chat.id)) + 1
            add_or_create_queue(
                str(message.chat.id),
                from_user=str(message.from_user.id),
                date=str(datetime.now()),
                file=file_name,
                type_of="song_file",
                position=position,
            )
            return await _message.edit(
                f"__Added to queue at {position} \n\n Title: [{type_of}]({file})\nDuration: {duration} Minutes\n Requested by:__ [{data['first_name']}]({data['mention']})",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("cʟᴏꜱᴇ", callback_data="close")]]
                ),
            )
        if str(message.chat.id) not in get_queues():
            add_or_create_queue(
                str(message.chat.id),
                from_user=str(message.from_user.id),
                date=str(datetime.now()),
                is_playing=True,
                file=file_name,
                type_of="song_file",
            )

        await _message.edit("💾 **__Downloading...__**")
        media = await client.download_media(
            message.reply_to_message,
            file_name=file_name,
            progress=progress,
            progress_args=(client, message.chat.id, _message.id),
        )
        if VOICE_CHATS.get(message.chat.id) is None:
            await _message.edit("🪄 **__Joining the voice chat...__**")
            VOICE_CHATS[message.chat.id] = tgcalls.get_group_call()
            await VOICE_CHATS[message.chat.id].start(message.chat.id)
        await sleep(2)
        await VOICE_CHATS[message.chat.id].start_audio(media, repeat=False)
        await _message.delete()
        await kreacher.send_photo(
            message.chat.id,
            caption=f"**__Started Streaming__**\n\n **Title:** [{type_of}]({file})\n **Requested by:** [{data['first_name']}]({data['mention']})",
            photo=fotoplay,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⏪", callback_data="back"),
                        InlineKeyboardButton(
                            "⏸️",
                            callback_data="pause_or_resume",
                        ),
                        InlineKeyboardButton(
                            "⏭️",
                            callback_data="next",
                        ),
                    ],
                ]
            ),
        )
        return await _message.pin()
    except Exception as err:
        logging.error(err)
        await _message.edit(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {err}`",
        )
        if message.chat.id in VOICE_CHATS:
            await VOICE_CHATS[message.chat.id].stop()
            remove_queue(str(message.chat.id))
            VOICE_CHATS.pop(message.chat.id)
