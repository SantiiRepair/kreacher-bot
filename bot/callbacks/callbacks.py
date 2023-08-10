import os
import pickle
from time import time
from bot import kreacher
from pyrogram import filters
from bot.config import config
from datetime import datetime
from pyrogram.enums.chat_type import ChatType
from bot.helpers.pkl import load_pkl, dump_pkl
from bot.instance_of.every_vc import VOICE_CHATS
from bot.helpers.pong import execution_time, START_TIME
from bot.helpers.handler import next_item, skip_current
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


thumb = "https://telegra.ph/file/3e14128ad5c9ec47801bd.jpg"

current_dir = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(current_dir, "../dbs/queues.pkl")

# Play Video Modes --------------------------------------------------------------------


# Play Song Modes ---------------------------------------------------------------------
@kreacher.on_callback_query(filters.regex("song_youtube_mode_callback"))
async def _(client, callback):
    start = time()
    current_time = datetime.utcnow()
    delta_ping = time() - start
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await execution_time(int(uptime_sec))
    await client.answer_callback_query(
        callback.id,
        text=f"{delta_ping * 1000:.3f}ms.\n\n Active since {uptime}",
        show_alert=True,
    )


@kreacher.on_callback_query(filters.regex("song_audio_or_voice_mode_callback"))
async def _(client, callback):
    start = time()
    current_time = datetime.utcnow()
    delta_ping = time() - start
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await execution_time(int(uptime_sec))
    await client.answer_callback_query(
        callback.id,
        text=f"{delta_ping * 1000:.3f}ms.\n\n Active since {uptime}",
        show_alert=True,
    )

# Streaming Controls -----------------------------------------------------------------
@kreacher.on_callback_query(filters.regex("pause_or_resume_callback"))
async def _(client, callback):
    chat = callback.chat
    if VOICE_CHATS[chat.id].is_video_paused:
        await VOICE_CHATS[chat.id].set_pause(False)
        return await callback.edit_message_text(
            "\U00002378 __Started Video Streaming!__",
            file=thumb,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "\u23EA", callback_data="back_callback"
                        ),
                        InlineKeyboardButton(
                            "\u25B6\uFE0F",
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
    await VOICE_CHATS[chat.id].set_pause(True)
    return await callback.edit_message_text(
        "\U00002378 __Started Video Streaming!__",
        file=thumb,
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
                [InlineKeyboardButton("cʟᴏꜱᴇ", callback_data="end_callback")],
            ]
        ),
    )


@kreacher.on_callback_query(filters.regex("back_callback"))
async def _(client, callback):
    chat = callback.chat
    await VOICE_CHATS[chat.id].set_pause(False)


@kreacher.on_callback_query(filters.regex("next_callback"))
async def _(client, callback):
    QUEUE = load_pkl(queues, "rb", "dict")
    chat = callback.chat
    if len(callback.text.split()) < 2:
        op = await skip_current(chat)
        if op == 0:
            await callback.reply("**Nothing Is Streaming**")
        elif op == 1:
            await callback.reply("empty queue, leaving voice chat")
        else:
            await callback.reply(
                f"**⏭ Skipped**\n**🎧 Now Playing** - [{op[0]}]({op[1]})",
                link_preview=False,
            )
    else:
        skip = callback.text.split(maxsplit=1)[1]
        DELQUE = "**Removing Following Songs From Queue:**"
        if chat.id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x != 0:
                    hm = await next_item(chat, x)
                    if hm != 0:
                        DELQUE = DELQUE + "\n" + f"**#{x}** - {hm}"
            await callback.reply(DELQUE)


@kreacher.on_callback_query(filters.regex("end_callback"))
async def _(client, callback):
    QUEUE = load_pkl(queues, "rb", "dict")
    chat = callback.chat
    QUEUE.pop(chat.id)
    dump_pkl(queues, "wb", QUEUE)
    await VOICE_CHATS[chat.id].stop_media()
    await VOICE_CHATS[chat.id].stop()
    VOICE_CHATS.pop(chat.id)


# Misc ----------------------------------------------------------------------------
@kreacher.on_callback_query(filters.regex("pong_callback"))
async def _(client, callback):
    start = time()
    current_time = datetime.utcnow()
    delta_ping = time() - start
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await execution_time(int(uptime_sec))
    await client.answer_callback_query(
        callback.id,
        text=f"{delta_ping * 1000:.3f}ms.\n\n Active since {uptime}",
        show_alert=True,
    )


@kreacher.on_callback_query(filters.regex("help"))
async def _(client, callback):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    await callback.edit_message_text(
        "ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ\n\nᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᴀᴅᴍɪɴ", callback_data="admin"),
                    InlineKeyboardButton("ᴘʟᴀʏ", callback_data="play"),
                ],
                [InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="start")],
            ]
        ),
    )


@kreacher.on_callback_query(filters.regex("admin"))
async def _(client, callback):
    await callback.edit_message_text(
        ADMIN_TEXT,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="help")]]
        ),
    )


@kreacher.on_callback_query(filters.regex("play"))
async def _(client, callback):
    await callback.edit_message_text(
        PLAY_TEXT,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="help")]]
        ),
    )


@kreacher.on_callback_query(filters.regex("start"))
async def _(client, callback):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    if callback.chat.type == ChatType.PRIVATE:
        await callback.edit_message_text(
            PM_START_TEXT(callback.sender.first_name),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardMarkup(
                            "\U0001F9D9 ᴀᴅᴅ ᴍᴇ",
                            url=f"https://t.me/{config:BOT_USERNAME}?startgroup=true",
                        ),
                        InlineKeyboardButton(
                            "/U0002753 ʜᴇʟᴘ", callback_data="help"
                        ),
                    ]
                ]
            ),
        )
        return


@kreacher.on_callback_query(filters.regex("cls"))
async def _(client, callback):
    return await callback.delete()


ADMIN_TEXT = """
**✘ A module from which admins of the chat can use!**

‣ `/end` - To End music streaming.
‣ `/skip` - To Skip Tracks Going on.
‣ `/pause` - To Pause streaming.
‣ `/resume` - to Resume Streaming.
‣ `/leavevc` - force The Userbot to leave Vc Chat (Sometimes Joined).
‣ `/playlist` - to check playlists.
"""

PLAY_TEXT = """
**✘ A module from which users of the chat can use!**

‣ `/play` - To play audio from else reply to audio file.
‣ `/vplay` - To stream videos in voice chat.
"""
