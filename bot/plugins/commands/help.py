from bot import kreacher
from pyrogram import filters, Client
from pyrogram.types import Message
from bot.config import config
from pyrogram.enums.chat_type import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@kreacher.on_message(filters.regex(pattern="^[!?/]help"))
async def _(client: Client, message: Message):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    if message.chat.type == ChatType.GROUP or ChatType.SUPERGROUP:
        await message.reply(
            "Contact me in PM to get available help menu!",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Help and Commands!",
                            url="t.me/{}?start=help".format(
                                config.BOT_USERNAME
                            ),
                        )
                    ]
                ]
            ),
        )
        return

    await message.reply(
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


@kreacher.on_message(filters.regex(pattern="^[!?/]start+help"))
async def _(client, message):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    await message.reply(
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
