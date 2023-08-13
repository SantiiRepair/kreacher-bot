import os
from bot import kreacher
from bot.helpers.pkl import load_pkl, dump_pkl
from bot.instance_of.every_vc import VOICE_CHATS
from bot.helpers.handler import next_item, skip_current
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

current_dir = os.path.dirname(os.path.abspath(__file__))
queues = os.path.join(current_dir, "../dbs/queues.pkl")


@kreacher.on_callback_query(filters.regex("pause_or_resume"))
async def _(client, callback):
    if VOICE_CHATS[callback.id].is_video_paused:
        await VOICE_CHATS[callback.id].set_pause(False)
        return await callback.edit_message_text(
            "\U00002378 __Started Video Streaming!__",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("\u23EA", callback_data="back"),
                        InlineKeyboardButton(
                            "\u25B6\uFE0F",
                            callback_data="pause_or_resume",
                        ),
                        InlineKeyboardButton(
                            "\u23ED\uFE0F", callback_data="next"
                        ),
                    ],
                    [InlineKeyboardButton("cʟᴏꜱᴇ", callback_data="controls")],
                ]
            ),
        )
    await VOICE_CHATS[callback.id].set_pause(True)
    return await callback.edit_message_text(
        "\U00002378 __Started Video Streaming!__",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("\u23EA", callback_data="back"),
                    InlineKeyboardButton(
                        "\u23F8\uFE0F",
                        callback_data="pause_or_resume",
                    ),
                    InlineKeyboardButton("\u23ED\uFE0F", callback_data="next"),
                ],
                [InlineKeyboardButton("cʟᴏꜱᴇ", callback_data="controls")],
            ]
        ),
    )


@kreacher.on_callback_query(filters.regex("back"))
async def _(client, callback):
    await VOICE_CHATS[callback.id].set_pause(False)


@kreacher.on_callback_query(filters.regex("next"))
async def _(client, callback):
    QUEUE = await load_pkl(queues, "rb", "dict")
    if len(callback.text.split()) < 2:
        op = await skip_current(callback)
        if op == 0:
            await callback.reply("**Nothing Is Streaming**")
        elif op == 1:
            await callback.reply("empty queue, leaving voice chat")
        else:
            await callback.reply(
                f"**⏭ Skipped**\n**🎧 Now Playing** - [{op[0]}]({op[1]})",
                link_preview=False,
            )
    else:
        skip = callback.text.split(maxsplit=1)[1]
        DELQUE = "**Removing Following Songs From Queue:**"
        if callback.id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x != 0:
                    hm = await next_item(callback, x)
                    if hm != 0:
                        DELQUE = DELQUE + "\n" + f"**#{x}** - {hm}"
            await callback.reply(DELQUE)


@kreacher.on_callback_query(filters.regex("controls"))
async def _(client, callback):
    QUEUE = await load_pkl(queues, "rb", "dict")
    QUEUE.pop(callback.id)
    dump_pkl(queues, "wb", QUEUE)
    await VOICE_CHATS[callback.id].stop_media()
    await VOICE_CHATS[callback.id].stop()
    VOICE_CHATS.pop(callback.id)
