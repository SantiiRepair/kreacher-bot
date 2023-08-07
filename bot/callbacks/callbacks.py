import os
import pickle
from bot import config, kreacher
from bot.instance.of_every_vc import VOICE_CHATS
from telethon import events, Button
from bot.helpers.handler import next_item, skip_current

thumb = "https://telegra.ph/file/3e14128ad5c9ec47801bd.jpg"

dir = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(dir, "../dbs/queues.pkl")


@kreacher.on(events.callbackquery.CallbackQuery(data="cls"))
async def _(event):
    await event.delete()


@kreacher.on(
    events.callbackquery.CallbackQuery(data="pause_or_resume_callback")
)
async def _(event):
    chat = await event.get_chat()
    if VOICE_CHATS[chat.id].is_video_paused:
        await VOICE_CHATS[chat.id].set_pause(False)
        return await event.edit(
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
    return await event.edit(
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
async def _(event):
    chat = await event.get_chat()
    await VOICE_CHATS[chat.id].set_pause(False)


@kreacher.on(events.callbackquery.CallbackQuery(data="next_callback"))
async def _(event):
    with open(queues, "r") as q:
        QUEUE = pickle.load(q)
    chat = await event.get_chat()
    if len(event.text.split()) < 2:
        op = await skip_current(chat)
        if op == 0:
            await event.reply("**Nothing Is Streaming**")
        elif op == 1:
            await event.reply("empty queue, leaving voice chat")
        else:
            await event.reply(
                f"**⏭ Skipped**\n**🎧 Now Playing** - [{op[0]}]({op[1]})",
                link_preview=False,
            )
    else:
        skip = event.text.split(maxsplit=1)[1]
        DELQUE = "**Removing Following Songs From Queue:**"
        if chat.id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x != 0:
                    hm = await next_item(chat, x)
                    if hm != 0:
                        DELQUE = DELQUE + "\n" + f"**#{x}** - {hm}"
            await event.reply(DELQUE)


@kreacher.on(events.callbackquery.CallbackQuery(data="end_callback"))
async def _(event):
    with open(queues, "r") as q:
        QUEUE = pickle.load(q)
    chat = await event.get_chat()
    QUEUE.pop(chat.id)
    with open(queues, "w") as q:
        pickle.dump(QUEUE, q)
    await VOICE_CHATS[chat.id].stop_media()
    await VOICE_CHATS[chat.id].stop()
    VOICE_CHATS.pop(chat.id)


@kreacher.on(events.callbackquery.CallbackQuery(data="help"))
async def _(event):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    await event.edit(
        "ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ\n\nᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`",
        buttons=[
            [
                Button.inline("ᴀᴅᴍɪɴ", data="admin"),
                Button.inline("ᴘʟᴀʏ", data="play"),
            ],
            [Button.inline("ʜᴏᴍᴇ", data="start")],
        ],
    )
