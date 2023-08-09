import os
import uuid
import logging
from asyncio import sleep
from pyrogram import filters
from bot.config import config
from bot.helpers.pkl import load_pkl
from bot.helpers.user_info import user_info
from bot import assistant, kreacher, on_call
from bot.helpers.progress import progress
from bot.helpers.yt import ytsearch, ytdl
from bot.instance_of.every_vc import VOICE_CHATS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.helpers.queues import (
    add_to_queue,
    clear_queue,
)


fotoplay = "https://telegra.ph/file/b6402152be44d90836339.jpg"
ngantri = "https://telegra.ph/file/b6402152be44d90836339.jpg"
owner = "1669178360"

current_dir = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(current_dir, "../dbs/queues.pkl")


@kreacher.on_message(filters.regex(pattern="^[!?/]play_song"))
async def play_song(client, message):
    QUEUE = load_pkl(queues, "rb", "dict")
    chat = message.chat
    title = " ".join(message.text[5:])
    replied = message.reply_to_message
    msg = await message.reply("\u23F3 **__Processing...__**")
    data = await user_info(message.from_user)
    await sleep(2)
    download_as = os.path.join(
        current_dir, f"../downloads/songs/{str(uuid.uuid4())}.mp3"
    )
    if not replied and not " " in message.message.text:
        await msg.edit(
            "❗ __Master, try with an: \n\nSending song name.\n\nYouTube video link.\n\nReply to an audio file.__",
        )
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
            reply_markup=[
                [InlineKeyboardButton("cʟᴏꜱᴇ", callback_data="cls")]
            ],
        )
    if VOICE_CHATS.get(chat.id) is None:
        try:
            await msg.edit("\U0001fa84 **__Joining the voice chat...__**")
            await on_call.join(chat.id)
            VOICE_CHATS[chat.id] = on_call
            await sleep(2)
        except Exception as e:
            await msg.edit(
                f"__Oops master, something wrong has happened.__ \n\n`Error: {e}`",
            )
            await VOICE_CHATS[chat.id].stop()
            VOICE_CHATS.pop(chat.id)
            await sleep(2)
    if replied and not replied.audio and not replied.voice or not replied:
        query = message.text.split(maxsplit=1)[1]
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
                    f"__Added to queue at {pos}\n\n Title: [{name}]({url})\nDuration: {duration} Minutes\n Requested by:__ [{data['first_name']}]({data['linked']})",
                    # file=thumb,
                    reply_markup=[
                        [InlineKeyboardButton("cʟᴏꜱᴇ", callback_data="cls")]
                    ],
                )

                try:
                    await on_call.start_audio(url, repeat=False)
                    add_to_queue(chat, name, url, ref, "audio")
                    await sleep(2)
                    await msg.edit(
                        f"**__Started Streaming__**\n\n **Title**: [{name}]({url})\n **Duration:** {duration} **Minutes\n Requested by:** [{data['first_name']}]({data['linked']})",
                        # file=thumb,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "\u23EA", callback_data="back_callback"
                                    ),
                                    InlineKeyboardButton(
                                        "\u23F8\uFE0F",
                                        callback_data="pause_or_resume_callback",
                                    ),
                                    InlineKeyboardButton(
                                        "\u23ED\uFE0F",
                                        callback_data="next_callback",
                                    ),
                                ],
                                [
                                    InlineKeyboardButton(
                                        "cʟᴏꜱᴇ", callback_data="end_callback"
                                    )
                                ],
                            ]
                        ),
                    )
                except Exception as e:
                    logging.error(e)
                    clear_queue(chat)
                    await VOICE_CHATS[chat.id].stop()
                    await msg.edit(
                        f"__Oops master, something wrong has happened.__ \n\n`Error: {e}`",
                    )
                    VOICE_CHATS.pop(chat.id)
                    return await sleep(2)

    else:
        try:
            if replied.audio:
                name = "Audio File"
                await msg.edit("\U0001f4be **__Downloading...__**")
                media = await client.download_media(
                    replied.audio,
                    file_name=download_as,
                    progress=progress,
                    progress_args=(client, chat, msg),
                )
            elif replied.voice:
                name = "Voice Note"
                await msg.edit("\U0001f4be **__Downloading...__**")
                media = await assistant.download_media(
                    replied.voice,
                    file_name=download_as,
                    progress=progress,
                    progress_args=(client, chat, msg),
                )
        except Exception as e:
            logging.error(e)
            return await msg.edit(
                f"__Oops master, something wrong has happened.__ \n\n`Error: {e}`",
            )
        proto = f"https://t.me/c/{chat.id}/{message.reply_to_message.id}"
        msg_linked = proto.replace("/c/-100", "/c/")
        if chat.id in QUEUE:
            # pos = add_to_queue(chat, name, url, ref, "audio")
            await msg.delete()
            await kreacher.send_photo(
                chat.id,
                caption=f"**__Added to queue at__** \n\n **Title:** [{name}]({msg_linked})\n **Requested by:** [{data['first_name']}]({data['linked']})",
                photo=ngantri,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "\u23EA", callback_data="back_callback"
                            ),
                            InlineKeyboardButton(
                                "\u23F8\uFE0F",
                                callback_data="pause_or_resume_callback",
                            ),
                            InlineKeyboardButton(
                                "\u23ED\uFE0F", callback_data="next_callback"
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                "cʟᴏꜱᴇ", callback_data="end_callback"
                            )
                        ],
                    ]
                ),
            )
        else:
            try:
                await sleep(2)
                await on_call.start_audio(media, repeat=False)
                await msg.delete()
                await kreacher.send_photo(
                    chat.id,
                    caption=f"**__Started Streaming__**\n\n **Title:** [{name}]({msg_linked})\n **Requested by:** [{data['first_name']}]({data['linked']})",
                    photo=fotoplay,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "\u23EA", callback_data="back_callback"
                                ),
                                InlineKeyboardButton(
                                    "\u23F8\uFE0F",
                                    callback_data="pause_or_resume_callback",
                                ),
                                InlineKeyboardButton(
                                    "\u23ED\uFE0F",
                                    callback_data="next_callback",
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    "cʟᴏꜱᴇ", callback_data="end_callback"
                                )
                            ],
                        ]
                    ),
                )
            except Exception as e:
                logging.error(e)
                clear_queue(chat)
                await VOICE_CHATS[chat.id].stop()
                await msg.edit(
                    f"__Oops master, something wrong has happened.__ \n\n`Error: {e}`",
                )
                VOICE_CHATS.pop(chat.id)
                return await sleep(2)
