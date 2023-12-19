package commands

from pyrogram.types import Message
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import kreacher


@kreacher.on_message(filters.regex(pattern="^[!?/]ping"))
async def _(client: Client, message: Message):
    return await message.reply(
        "**__PONG!!__**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("\U0001f3d3", callback_data="pong")]]
        ),
    )
