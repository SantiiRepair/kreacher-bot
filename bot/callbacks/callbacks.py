import os
import pickle
from bot import kreacher
from bot.config import config
from bot.instance_of.every_vc import VOICE_CHATS
from telethon import events, Button
from bot.helpers.handler import next_item, skip_current
from bot.helpers.pkl import load_pkl, dump_pkl

thumb = "https://telegra.ph/file/3e14128ad5c9ec47801bd.jpg"

dir = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(dir, "../dbs/queues.pkl")


@kreacher.on(events.callbackquery.CallbackQuery(data="cls"))
async def _(message):
    await message.delete()


@kreacher.on(
    events.callbackquery.CallbackQuery(data="pause_or_resume_callback")
)
async def _(message):
    chat = await message.get_chat()
    if VOICE_CHATS[chat.id].is_video_paused:
        await VOICE_CHATS[chat.id].set_pause(False)
        return await message.edit(
            "\U00002378 __Started Video Streaming!__",
            file=thumb,
            buttons=[
                [
                    Button.inline("\u23EA", data="back_callback"),
                    Button.inline(
                        "\u25B6\uFE0F", data="pause_or_resume_callback"
                    ),
                    Button.inline("\u23ED\uFE0F", data="next_callback"),
                ],
                [Button.inline("cʟᴏꜱᴇ", data="end_callback")],
            ],
        )
    await VOICE_CHATS[chat.id].set_pause(True)
    return await message.edit(
        "\U00002378 __Started Video Streaming!__",
        file=thumb,
        buttons=[
            [
                Button.inline("\u23EA", data="back_callback"),
                Button.inline("\u23F8\uFE0F", data="pause_or_resume_callback"),
                Button.inline("\u23ED\uFE0F", data="next_callback"),
            ],
            [Button.inline("cʟᴏꜱᴇ", data="end_callback")],
        ],
    )


@kreacher.on(events.callbackquery.CallbackQuery(data="back_callback"))
async def _(message):
    chat = await message.get_chat()
    await VOICE_CHATS[chat.id].set_pause(False)


@kreacher.on(events.callbackquery.CallbackQuery(data="next_callback"))
async def _(message):
    QUEUE = load_pkl(queues, "rb", "dict")
    chat = await message.get_chat()
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


@kreacher.on(events.callbackquery.CallbackQuery(data="end_callback"))
async def _(message):
    QUEUE = load_pkl(queues, "rb", "dict")
    chat = await message.get_chat()
    QUEUE.pop(chat.id)
    dump_pkl(queues, "wb", QUEUE)
    await VOICE_CHATS[chat.id].stop_media()
    await VOICE_CHATS[chat.id].stop()
    VOICE_CHATS.pop(chat.id)


@kreacher.on(events.callbackquery.CallbackQuery(data="help"))
async def _(message):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    await message.edit(
        "ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ\n\nᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`",
        buttons=[
            [
                Button.inline("ᴀᴅᴍɪɴ", data="admin"),
                Button.inline("ᴘʟᴀʏ", data="play"),
            ],
            [Button.inline("ʜᴏᴍᴇ", data="start")],
        ],
    )


@kreacher.on(events.callbackquery.CallbackQuery(data="admin"))
async def _(message):
    await message.edit(
        ADMIN_TEXT, buttons=[[Button.inline("« Bᴀᴄᴋ", data="help")]]
    )


@kreacher.on(events.callbackquery.CallbackQuery(data="play"))
async def _(message):
    await message.edit(
        PLAY_TEXT, buttons=[[Button.inline("« Bᴀᴄᴋ", data="help")]]
    )


@kreacher.on(events.callbackquery.CallbackQuery(data="start"))
async def _(message):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    if message.is_private:
        await message.edit(
            PM_START_TEXT(message.sender.first_name),
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
