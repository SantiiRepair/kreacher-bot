from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums.chat_type import ChatType
from bot import kreacher
from pyrogram import filters
from bot.config import config


def PM_START_TEXT(name):
    return (
        """__Helo my dear master %s__ \U0001F9D9

__I am Kreacher, the house-elf of the family Black. you have call me, and I am here to begrudginly assist you in sharing you songs and videos in Telegram voice chat.

To summon me, simply send the command /vplay followed by the link of the video you wish to share. I will take care of playing it to all members of the voice chat, wheter I like it or not.

If you require further instruction, you can use this command /help to learn more about how to use my begrudging service.

It is my... pleasure... to serve you, my dear wizard or witch master.

Have a... tolerable... day!__ \U0001F52E
"""
        % name
    )


@kreacher.on_message(filters.regex(pattern="^[!?/]start"))
async def _(client, message):
    chat = message.chat
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    if message.chat.type == ChatType.PRIVATE:
        return await kreacher.send_photo(
            chat.id,
            photo=config.START_IMG,
            caption=PM_START_TEXT(message.from_user.first_name),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "\U0001F9D9 ᴀᴅᴅ ᴍᴇ",
                            url=f"https://t.me/{config.BOT_USERNAME}?startgroup=true",
                        ),
                        InlineKeyboardButton(
                            "/U00002753 ʜᴇʟᴘ", callback_data="help"
                        ),
                    ]
                ]
            ),
        )

    if message.chat.type == ChatType.GROUP or ChatType.SUPERGROUP:
        return await message.reply("**ʜᴇʏ! ɪ'ᴍ ꜱᴛɪʟʟ ᴀʟɪᴠᴇ ✅**")
