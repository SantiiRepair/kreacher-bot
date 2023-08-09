import os
import pickle
import datetime
from time import time
from bot import kreacher
from pyrogram import filters
from bot.config import config
from bot.helpers.pong import execution_time
from bot.helpers.pkl import load_pkl, dump_pkl
from bot.instance_of.every_vc import VOICE_CHATS
from bot.helpers.handler import next_item, skip_current
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


thumb = "https://telegra.ph/file/3e14128ad5c9ec47801bd.jpg"

dir = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(dir, "../dbs/queues.pkl")


@kreacher.on_callback_query(filters.regex("cls"))
async def _(message):
    await message.delete()


@kreacher.on_callback_query(filters.regex("pause_or_resume_callback"))
async def _(client, message):
    chat = message.chat
    if VOICE_CHATS[chat.id].is_video_paused:
        await VOICE_CHATS[chat.id].set_pause(False)
        return await message.edit(
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
    return await message.edit(
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
async def _(client, message):
    chat = message.chat
    await VOICE_CHATS[chat.id].set_pause(False)


@kreacher.on_callback_query(filters.regex("next_callback"))
async def _(client, message):
    QUEUE = load_pkl(queues, "rb", "dict")
    chat = message.chat
    if len(message.text.split()) < 2:
        op = await skip_current(chat)
        if op == 0:
            await message.reply("**Nothing Is Streaming**")
        elif op == 1:
            await message.reply("empty queue, leaving voice chat")
        else:
            await message.reply(
                f"**⏭ Skipped**\n**🎧 Now Playing** - [{op[0]}]({op[1]})",
                link_preview=False,
            )
    else:
        skip = message.text.split(maxsplit=1)[1]
        DELQUE = "**Removing Following Songs From Queue:**"
        if chat.id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x != 0:
                    hm = await next_item(chat, x)
                    if hm != 0:
                        DELQUE = DELQUE + "\n" + f"**#{x}** - {hm}"
            await message.reply(DELQUE)


@kreacher.on_callback_query(filters.regex("end_callback"))
async def _(client, message):
    QUEUE = load_pkl(queues, "rb", "dict")
    chat = message.chat
    QUEUE.pop(chat.id)
    dump_pkl(queues, "wb", QUEUE)
    await VOICE_CHATS[chat.id].stop_media()
    await VOICE_CHATS[chat.id].stop()
    VOICE_CHATS.pop(chat.id)


@kreacher.on_callback_query(filters.regex("pong_callback"))
async def _(client, callback):
    chat = callback.message.chat
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
async def _(client, message):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    await message.edit(
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
async def _(client, message):
    await message.edit(
        ADMIN_TEXT,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="help")]]
        ),
    )


@kreacher.on_callback_query(filters.regex("play"))
async def _(client, message):
    await message.edit(
        PLAY_TEXT,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="help")]]
        ),
    )


@kreacher.on_callback_query(filters.regex("start"))
async def _(client, message):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    if message.is_private:
        await message.edit(
            PM_START_TEXT(message.sender.first_name),
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
