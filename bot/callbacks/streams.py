import os
from pyrogram import filters, Client
from pyrogram.types import CallbackQuery
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import kreacher, VOICE_CHATS
from bot.decorators.permissions import only_admins_or_requester
from bot.helpers.queues import (
    get_queues,
    next_in_queue,
    previous_in_queue,
    remove_queue,
)


_cwd = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(_cwd, "../dbs/queues.pkl")


@kreacher.on_callback_query(filters.regex("pause_or_resume"))
@only_admins_or_requester
async def _(client: Client, callback: CallbackQuery):
    if VOICE_CHATS[callback.message.chat.id].is_video_paused:
        await VOICE_CHATS[callback.message.chat.id].set_pause(False)
        return await callback.edit_message_reply_markup(
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
                    InlineKeyboardButton("sᴛᴏᴘ ᴀʟʟ", callback_data="quit"),
                ]
            ),
        )
    await VOICE_CHATS[callback.message.chat.id].set_pause(True)
    return await callback.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏪", callback_data="back"),
                    InlineKeyboardButton(
                        "▶️",
                        callback_data="pause_or_resume",
                    ),
                    InlineKeyboardButton("⏭️", callback_data="next"),
                ],
                InlineKeyboardButton("sᴛᴏᴘ ᴀʟʟ", callback_data="quit"),
            ]
        ),
    )


@kreacher.on_callback_query(filters.regex("back"))
async def _(client: Client, callback: CallbackQuery):
    chat = callback.message.chat
    await VOICE_CHATS[chat.id].set_pause(False)


@kreacher.on_callback_query(filters.regex("next"))
async def _(client: Client, callback: CallbackQuery):
    await callback.reply(
        f"**⏭ Skipped**\n**🎧 Now Playing**",
        link_preview=False,
    )
    this = callback.text.split(maxsplit=1)[1]
    if callback.message.chat.id in get_queues():
        DELQUE = "**Removing Following Songs From Queue:**"
        await callback.reply(DELQUE)


@kreacher.on_callback_query(filters.regex("remove_queues"))
async def _(client: Client, callback: CallbackQuery):
    remove_queue(str(callback.message.chat))
    await VOICE_CHATS[callback.message.chat.id].stop_media()
    await VOICE_CHATS[callback.message.chat.id].stop()
    VOICE_CHATS.pop(callback.message.chat.id)
