import os
import re
import uuid
import logging
from asyncio import sleep
from pyrogram import filters, Client
from pyrogram.types import Message
from bot.helpers.pkl import load_pkl
from bot.helpers.user_info import user_info
from bot import kreacher, on_call
from bot.helpers.progress import progress
from bot.helpers.yt import ytsearch, ytdl
from bot.dbs.instances import VOICE_CHATS
from pyrogram.enums.chat_type import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.helpers.queues import (
    clear_queue,
)


fotoplay = "https://telegra.ph/file/b6402152be44d90836339.jpg"
ngantri = "https://telegra.ph/file/b6402152be44d90836339.jpg"
owner = "1669178360"

c = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(c, "../../dbs/queues.pkl")


@kreacher.on_message(filters.regex(pattern="^[!?/]play_song"))
async def _(client: Client, message: Message):
    QUEUE = await load_pkl(queues, "rb", "dict")
    data = await user_info(message.from_user)
    download_as = os.path.join(c, f"../../downloads/songs/{str(uuid.uuid4())}.mp3")
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply(
            "**__Mr. Wizard, this command can only be used in groups or channels__** \U0001f937\U0001f3fb\u200D\u2642\uFE0F"
        )
    if not message.reply_to_message and " " not in message.text:
        return await message.reply(
            "**__How to use this command.\n\nNext we show two ways to use this command, click on the button with the mode you are looking for to know details.__**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "sᴇᴀʀᴄʜ",
                            callback_data="search_song_mode",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "ʏᴏᴜᴛᴜʙᴇ",
                            callback_data="youtube_song_mode",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "ᴀᴜᴅɪᴏ",
                            callback_data="audio_song_mode",
                        )
                    ],
                ],
            ),
        )
    msg = await message.reply("\u23F3 **__Processing...__**")
    await sleep(2)
    try:
        if " " in message.text:
            query = message.text.split(maxsplit=1)[1]
            if "http" in query:
                regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
                match = re.match(regex, query)
                if not match:
                    return await msg.edit(
                        "**__Sorry, but this doesn't seem to be a YouTube link__** \U0001f914"
                    )
            search = await ytsearch(query)
            name = search[0]
            ref = search[1]
            duration = search[2]
            # thumb = await gen_thumb(videoid)
            fmt = "best[height<=?720][width<=?1280]"
            hm, url = await ytdl(fmt, ref)
            if hm == 0:
                await msg.edit(f"`{url}`")
            if search == 0:
                return await msg.edit(
                    "__Can't find song.\n\nTry searching with more specific title.__",
                )
            if message.chat.id in QUEUE:
                # pos = await add_to_queue(message.chat, name, url, ref, "audio")
                return await msg.edit(
                    f"__Added to queue at \n\n Title: [{name}]({url})\nDuration: {duration} Minutes\n Requested by:__ [{data['first_name']}]({data['mention']})",
                    # file=thumb,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("cʟᴏꜱᴇ", callback_data="cls")]]
                    ),
                )
            if VOICE_CHATS.get(message.chat.id) is None:
                await msg.edit("🪄 **__Joining the voice chat...__**")
                await on_call.join(message.chat.id)
                VOICE_CHATS[message.chat.id] = on_call
            await sleep(2)
            await on_call.start_audio(url, repeat=False)
            # await add_to_queue(message.chat, name, url, ref, "audio")
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
        if message.reply_to_message and message.reply_to_message.audio:
            name = "Audio File"
            await msg.edit("💾 **__Downloading...__**")
            media = await client.download_media(
                message.reply_to_message.audio,
                file_name=download_as,
                progress=progress,
                progress_args=(client, message.chat, msg),
            )
        elif message.reply_to_message and message.reply_to_message.voice:
            name = "Voice Note"
            await msg.edit("💾 **__Downloading...__**")
            media = await client.download_media(
                message.reply_to_message.voice,
                file_name=download_as,
                progress=progress,
                progress_args=(client, message.chat, msg),
            )
        proto = f"https://t.me/c/{message.chat.id}/{message.reply_to_message.id}"
        msg_mention = proto.replace("/c/-100", "/c/")
        if message.chat.id in QUEUE:
            # pos = add_to_queue(message.chat, name, url, ref, "audio")
            await msg.delete()
            return await kreacher.send_photo(
                message.chat.id,
                caption=f"**__Added to queue at__** \n\n **Title:** [{name}]({msg_mention})\n **Requested by:** [{data['first_name']}]({data['mention']})",
                photo=ngantri,
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
                        [
                            InlineKeyboardButton(
                                "\U0001f52e ᴄᴏɴᴛʀᴏʟs", callback_data="controls"
                            )
                        ],
                    ]
                ),
            )
        if VOICE_CHATS.get(message.chat.id) is None:
            await msg.edit("🪄 **__Joining the voice chat...__**")
            await on_call.join(message.chat.id)
            VOICE_CHATS[message.chat.id] = on_call
        await sleep(2)
        await on_call.start_audio(media, repeat=False)
        await msg.delete()
        await kreacher.send_photo(
            message.chat.id,
            caption=f"**__Started Streaming__**\n\n **Title:** [{name}]({msg_mention})\n **Requested by:** [{data['first_name']}]({data['mention']})",
            photo=fotoplay,
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
    except Exception as e:
        logging.error(e)
        await msg.edit(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
        if message.chat.id in VOICE_CHATS:
            await VOICE_CHATS[message.chat.id].stop()
            await clear_queue(message.chat)
            VOICE_CHATS.pop(message.chat.id)
