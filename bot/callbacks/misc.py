import os
from pyrogram import filters
from time import time
from bot import kreacher
from bot.config import config
from datetime import datetime
from pyrogram.enums.chat_type import ChatType
from bot.helpers.pong import execution_time, START_TIME
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


thumb = "https://telegra.ph/file/3e14128ad5c9ec47801bd.jpg"

current_dir = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(current_dir, "../dbs/queues.pkl")


@kreacher.on_callback_query(filters.regex("song_youtube_mode"))
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


@kreacher.on_callback_query(filters.regex("song_audio_or_voice_mode"))
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


@kreacher.on_callback_query(filters.regex("pong"))
async def _(client, callback):
    start = time()
    current_time = datetime.utcnow()
    delta_ping = time() - start
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await execution_time(int(uptime_sec))
    await client.answer_callback_query(
        callback.id,
        text=f"{delta_ping * 1000:.3f}ms.\n\nActive since {uptime}",
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
        return await callback.edit_message_text(
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
