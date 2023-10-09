import os
from time import time
from bot import kreacher
from datetime import datetime
from pyrogram import filters, Client
from pyrogram.types import CallbackQuery
from pyrogram.enums.chat_type import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.config import config
from bot.__main__ import execution_time, START_TIME
from bot.plugins.commands.start import PM_START_TEXT

thumb = "https://telegra.ph/file/3e14128ad5c9ec47801bd.jpg"

current_dir = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(current_dir, "../dbs/queues.pkl")


@kreacher.on_callback_query(filters.regex("song_youtube_mode"))
async def _(client: Client, callback: CallbackQuery):
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
async def _(client: Client, callback: CallbackQuery):
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
async def _(client: Client, callback: CallbackQuery):
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
async def _(client: Client, callback: CallbackQuery):
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


@kreacher.on_callback_query(filters.regex("start"))
async def _(client: Client, callback: CallbackQuery):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    if callback.chat.type == ChatType.PRIVATE:
        return await callback.edit_message_text(
            PM_START_TEXT(callback.sender.first_name),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "\U0001F9D9 ᴀᴅᴅ ᴍᴇ",
                            url=f"https://t.me/{config:BOT_USERNAME}?startgroup=true",
                        ),
                        InlineKeyboardButton("/U0002753 ʜᴇʟᴘ", callback_data="help"),
                    ]
                ]
            ),
        )


@kreacher.on_callback_query(filters.regex("close"))
async def _(client: Client, callback: CallbackQuery):
    return await callback.delete()
