from telethon import events, Button
from kreacher import kreacher, config


@kreacher.on(events.NewMessage(pattern="[!?/]help"))
async def help(event):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    if event.is_group:
        await event.reply(
            "Contact me in PM to get available help menu!",
            buttons=[
                [
                    Button.url(
                        "Help and Commands!",
                        "t.me/{}?start=help".format(config.BOT_USERNAME),
                    )
                ]
            ],
        )
        return

    await event.reply(
        "ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ\n\nᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`",
        buttons=[
            [
                Button.inline("ᴀᴅᴍɪɴ", data="admin"),
                Button.inline("ᴘʟᴀʏ", data="play"),
            ],
            [Button.inline("ʜᴏᴍᴇ", data="start")],
        ],
    )


@kreacher.on(events.NewMessage(pattern="^/start help"))
async def _(event):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    await event.reply(
        "ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ\n\nᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`",
        buttons=[
            [
                Button.inline("ᴀᴅᴍɪɴ", data="admin"),
                Button.inline("ᴘʟᴀʏ", data="play"),
            ],
            [Button.inline("ʜᴏᴍᴇ", data="start")],
        ],
    )
