from telethon import events, Button
from kreacher import kreacher, config


btn = [
    [Button.inline("ᴀᴅᴍɪɴ", data="admin"), Button.inline("ᴘʟᴀʏ", data="play")],
    [Button.inline("ʜᴏᴍᴇ", data="start")],
]

HELP_TEXT = "ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ\n\nᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`"


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

    await event.reply(HELP_TEXT, buttons=btn)


@kreacher.on(events.NewMessage(pattern="^/start help"))
async def _(event):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    await event.reply(HELP_TEXT, buttons=btn)


@kreacher.on(events.callbackquery.CallbackQuery(data="help"))
async def _(event):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    await event.edit(HELP_TEXT, buttons=btn)
