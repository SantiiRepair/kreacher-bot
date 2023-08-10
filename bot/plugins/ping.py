from bot import kreacher
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@kreacher.on_message(filters.regex(pattern="^[!?/]ping"))
async def _(client, message):
    await message.reply(
        "**__PONG!!__**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "\U0001f3d3", callback_data="pong_callback"
                    )
                ]
            ]
        ),
    )
    await message.delete()
