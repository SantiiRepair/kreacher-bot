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
from bot import assistant, kreacher, tgcalls, VOICE_CHATS
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
        msg = await message.reply("\u23F3 **__Processing...__**")
        await sleep(2)
        file_name = f"/tmp/{str(uuid.uuid4())}.mp4"
        if not message.reply_to_message and " " not in message.text:
            return await msg.edit(
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
                    return await msg.edit(
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
                await msg.edit("🔄 **__Starting live video stream...__**")
                await sleep(2)
                await VOICE_CHATS[message.chat.id].start_video(
                    query,
                    enable_experimental_lip_sync=True,
                    repeat=False,
                )
                # await msg.delete()
                await msg.edit(
                    "\U00002378 **Started video streaming!**",
                    # photo=thumb,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("\u23EA", callback_data="back"),
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
                return await msg.pin()
            regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
            match = re.match(regex, query)
            if "http" in query and not match:
                return await msg.edit(
                    "**__Sorry, but this doesn't seem to be a YouTube link__** \U0001f914"
                )
            search = await ytsearch(query)
            name = search[0]
            ref = search[1]
            duration = search[2]
            fmt = "best[height<=?720][width<=?1280]"
            _, url = await ytdl(fmt, ref)
            if search == 0:
                return await msg.edit(
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
                return await msg.edit(
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
                await msg.edit("🪄 **__Joining the voice chat...__**")
                await tgcalls.start(message.chat.id)
                VOICE_CHATS[message.chat.id] = tgcalls
            await sleep(2)
            await VOICE_CHATS[message.chat.id].start_video(
                url,
                enable_experimental_lip_sync=True,
                repeat=False,
            )
            await msg.edit(
                f"**__Started Streaming__**\n\n **Title**: [{name}]({url})\n **Duration:** {duration} **Minutes\n Requested by:** [{data['first_name']}]({data['mention']})",
                # file=thumb,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("\u23EA", callback_data="back"),
                            InlineKeyboardButton(
                                "\u23F8\uFE0F",
                                callback_data="pause_or_resume",
                            ),
                            InlineKeyboardButton(
                                "\u23ED\uFE0F",
                                callback_data="next",
                            ),
                        ],
                    ]
                ),
            )
            return await msg.pin()
        if message.reply_to_message.video or message.reply_to_message.file:
            await msg.edit("🔄 **__Downloading...__**")
            media = await assistant.download_media(
                message.reply_to_message.video,
                file_name=file_name,
                progress=progress,
                progress_args=(client, message.chat, msg),
            )
            if str(message.chat.id) in get_queues():
                position = get_last_position_in_queue(str(message.chat.id)) + 1
                add_or_create_queue(
                    str(message.chat.id),
                    from_user=str(message.from_user.id),
                    date=str(datetime.now()),
                    file=media,
                    type_of="video_media",
                    position=position,
                )
                return await msg.edit(
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
                    file=media,
                    type_of="video_media",
                )
            if VOICE_CHATS.get(message.chat.id) is None:
                await msg.edit("**__Joining the voice chat...__** \u23F3")
                await tgcalls.start(message.chat.id)
                VOICE_CHATS[message.chat.id] = tgcalls
                await sleep(2)
            await VOICE_CHATS[message.chat.id].start_video(
                media, enable_experimental_lip_sync=True, repeat=False
            )
            # await msg.delete()
            await msg.edit(
                "**Started video streaming!**",
                # photo=thumb,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("\u23EA", callback_data="back"),
                            InlineKeyboardButton(
                                "\u23F8\uFE0F",
                                callback_data="pause_or_resume",
                            ),
                            InlineKeyboardButton("\u23ED\uFE0F", callback_data="next"),
                        ],
                    ],
                ),
            )
    except Exception as err:
        logging.error(err)
        await msg.edit(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {err}`",
        )
        if message.chat.id in VOICE_CHATS:
            await VOICE_CHATS[message.chat.id].stop()
            remove_queue(str(message.chat.id))
            VOICE_CHATS.pop(message.chat.id)
