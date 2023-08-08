from bot import kreacher
from bot.config import config
from telethon import events, Button


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


@kreacher.on(events.NewMessage(pattern="[!?/]start"))
async def start(event):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    if event.is_private:
        await event.client.send_file(
            event.chat_id,
            config.START_IMG,
            caption=PM_START_TEXT(event.sender.first_name),
            buttons=[
                [
                    Button.url(
                        "\U0001F9D9 ᴀᴅᴅ ᴍᴇ",
                        f"https://t.me/{config.BOT_USERNAME}?startgroup=true",
                    ),
                    Button.inline("/U00002753 ʜᴇʟᴘ", data="help"),
                ]
            ],
        )
        return

    if event.is_group:
        await event.reply("**ʜᴇʏ! ɪ'ᴍ ꜱᴛɪʟʟ ᴀʟɪᴠᴇ ✅**")
        return


@kreacher.on(events.callbackquery.CallbackQuery(data="start"))
async def _(event):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    if event.is_private:
        await event.edit(
            PM_START_TEXT(event.sender.first_name),
            buttons=[
                [
                    Button.url(
                        "\U0001F9D9 ᴀᴅᴅ ᴍᴇ",
                        f"https://t.me/{config:BOT_USERNAME}?startgroup=true",
                    ),
                    Button.inline("/U0002753 ʜᴇʟᴘ", data="help"),
                ]
            ],
        )
        return
