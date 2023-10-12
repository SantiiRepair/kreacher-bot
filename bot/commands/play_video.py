import re
import uuid
import logging
from asyncio import sleep
from datetime import datetime
from pyrogram.types import Message
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from bot.helpers.progress import progress
from bot.helpers.yt import ytdl, ytsearch
from bot.helpers.user_info import user_info
from bot import kreacher, tgcalls, userbot, VOICE_CHATS
from bot.helpers.queues import (
    add_or_create_queue,
    get_queues,
    get_last_position_in_queue,
    remove_queue,
)

fotoplay = "https://telegra.ph/file/b6402152be44d90836339.jpg"
ngantri = "https://telegra.ph/file/b6402152be44d90836339.jpg"
thumb = "https://telegra.ph/file/3e14128ad5c9ec47801bd.jpg"


@kreacher.on_message(filters.regex(pattern="^[!?/]play_video"))
async def _(client: Client, message: Message):
    data = await user_info(message.from_user)
    try:
        _message = await message.reply("\u23F3 **__Processing...__**")
        await sleep(2)
        file_name = f"/tmp/{str(uuid.uuid4())}.mp4"
        if not message.reply_to_message and " " not in message.text:
            return await _message.edit(
                "❗ __Master, try with an: \n\nLive stream link.\n\nYouTube video/ link.\n\nReply to an video to start video streaming!__",
            )

        if " " in message.text:
            query = message.text.split(maxsplit=1)[1]
            if "cdn" in query:
                if str(message.chat.id) in get_queues():
                    position = get_last_position_in_queue(str(message.chat.id)) + 1
                    add_or_create_queue(
                        str(message.chat.id),
                        from_user=str(message.from_user.id),
                        date=str(datetime.now()),
                        file=query,
                        type_of="video_stream",
                        position=position,
                    )
                    return await _message.edit(
                        f"__Added to queue at {position} \n\n Title: [{name}]({query})\nDuration: {duration} Minutes\n Requested by:__ [{data['first_name']}]({data['mention']})",
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
                        file=query,
                        type_of="video_stream",
                    )
                await _message.edit("🔄 **__Starting live video stream...__**")
                await sleep(2)
                await VOICE_CHATS[message.chat.id].start_video(
                    query,
                    enable_experimental_lip_sync=True,
                    repeat=False,
                )
                # await _message.delete()
                await _message.edit(
                    "\U00002378 **Started video streaming!**",
                    # photo=thumb,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("⏪", callback_data="back"),
                                InlineKeyboardButton(
                                    "\u23F8\uFE0F",
                                    callback_data="pause_or_resume",
                                ),
                                InlineKeyboardButton("⏭️", callback_data="next"),
                            ],
                        ],
                    ),
                )
                return await _message.pin()
            regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
            match = re.match(regex, query)
            if "http" in query and not match:
                return await _message.edit(
                    "**__Sorry, but this doesn't seem to be a YouTube link__** \U0001f914"
                )
            search = await ytsearch(query)
            name = search[0]
            ref = search[1]
            duration = search[2]
            fmt = "best[height<=?720][width<=?1280]"
            _, url = await ytdl(fmt, ref)
            if search == 0:
                return await _message.edit(
                    "**__Can't find YouTube video.\n\nTry searching with more specific title.__**",
                )
            if str(message.chat.id) in get_queues():
                position = get_last_position_in_queue(str(message.chat.id)) + 1
                add_or_create_queue(
                    str(message.chat.id),
                    from_user=str(message.from_user.id),
                    date=str(datetime.now()),
                    file=url,
                    type_of="video_yt",
                    position=position,
                )
                return await _message.edit(
                    f"__Added to queue at {position} \n\n Title: [{name}]({url})\nDuration: {duration} Minutes\n Requested by:__ [{data['first_name']}]({data['mention']})",
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
                    type_of="video_yt",
                )
            if VOICE_CHATS.get(message.chat.id) is None:
                await _message.edit("🪄 **__Joining the voice chat...__**")
                await tgcalls.start(message.chat.id)
                VOICE_CHATS[message.chat.id] = tgcalls
            await sleep(2)
            await VOICE_CHATS[message.chat.id].start_video(
                url,
                enable_experimental_lip_sync=True,
                repeat=False,
            )
            await _message.edit(
                f"**__Started Streaming__**\n\n **Title**: [{name}]({url})\n **Duration:** {duration} **Minutes\n Requested by:** [{data['first_name']}]({data['mention']})",
                # file=thumb,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("⏪", callback_data="back"),
                            InlineKeyboardButton(
                                "\u23F8\uFE0F",
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
        if message.reply_to_message.video or message.reply_to_message.file:
            file_name = (
                f"/tmp/{str(uuid.uuid4())}.{message.reply_to_message.video.mime_type.split('/', 1)[1]}"
                if message.reply_to_message.video
                else f"/tmp/{str(uuid.uuid4())}.mp4"
            )
            type_of = "Video File"
            duration = (
                round((message.reply_to_message.video.duration / 60), 2)
                if message.reply_to_message.video
                else round((message.reply_to_message.file.duration / 60), 2)
            )
            file = f"https://t.me/c/{message.chat.id}/{message.reply_to_message.id}".replace(
                "/c/-100", "/c/"
            )
            if str(message.chat.id) in get_queues():
                position = get_last_position_in_queue(str(message.chat.id)) + 1
                add_or_create_queue(
                    str(message.chat.id),
                    from_user=str(message.from_user.id),
                    date=str(datetime.now()),
                    file=file_name,
                    type_of="video_media",
                    position=position,
                )
                return await _message.edit(
                    f"__Added to queue at {position}\n\nTitle: [{type_of}]({file})\nDuration: {duration} Minutes\nRequested by:__ [{data['first_name']}]({data['mention']})",
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
                    type_of="video_media",
                )
            await _message.edit("💾 **__Downloading...__**")
            media = await userbot.download_media(
                message.reply_to_message,
                file_name=file_name,
                progress=progress,
                progress_args=(client, message.chat.id, _message.id),
            )
            if VOICE_CHATS.get(message.chat.id) is None:
                await _message.edit("🪄 **__Joining the voice chat...__**")
                await tgcalls.start(message.chat.id)
                VOICE_CHATS[message.chat.id] = tgcalls
            await sleep(2)
            await VOICE_CHATS[message.chat.id].start_video(
                media,
                enable_experimental_lip_sync=True,
                repeat=False,
            )
            # await _message.delete()
            await _message.edit(
                "**Started video streaming!**",
                # photo=thumb,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("⏪", callback_data="back"),
                            InlineKeyboardButton(
                                "⏸️",
                                callback_data="pause_or_resume",
                            ),
                            InlineKeyboardButton("⏭️", callback_data="next"),
                        ],
                    ],
                ),
            )
    except Exception as err:
        logging.error(err)
        await _message.edit(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {err}`",
        )
        if message.chat.id in VOICE_CHATS:
            await VOICE_CHATS[message.chat.id].stop()
            remove_queue(str(message.chat.id))
            VOICE_CHATS.pop(message.chat.id)
