import os

import uuid
import logging
from asyncio import sleep
from bot.config import config
from pyrogram.types import Message
from difflib import SequenceMatcher
from pyrogram import filters, Client
from pyrogram.enums import MessagesFilter
from bot.helpers.progress import progress
from bot.dbs.instances import VOICE_CHATS
from bot import assistant, kreacher, on_call
from bot.decorators.only_grps_chnns import only_grps_chnns
from bot.helpers.queues import (
    clear_queue,
)

current_dir = os.path.dirname(os.path.abspath(__file__))


@kreacher.on_message(filters.regex(pattern="^[!?/]streaming"))
@only_grps_chnns
async def _(client: Client, message: Message):
    results = []
    try:
        if " " not in message.text:
            return await message.reply(
                "**__How to use this command.\n\nNext we show two ways to use this command, click on the button with the mode you are looking for to know details.__**"
            )
        msg = await message.reply("**__Searching...__**")
        await sleep(2)
        search = message.text.split(maxsplit=1)[1]
        movie_name = os.path.join(
            current_dir, f"../downloads/movies/{str(uuid.uuid4())}.mp4"
        )
        serie_name = os.path.join(
            current_dir, f"../downloads/series/{str(uuid.uuid4())}.mp4"
        )
        series_channel = await assistant.get_chat(config.ES_SERIES_CHANNEL)
        movies_channel = await assistant.get_chat(config.ES_MOVIES_CHANNEL)
        async for serie in assistant.search_messages(
            chat_id=series_channel.id,
            query=search,
            limit=1000,
            filter=MessagesFilter.VIDEO,
        ):
            results.append(f"{serie.video.file_id};{serie.caption};serie")
        async for movie in assistant.search_messages(
            chat_id=movies_channel.id,
            query=search,
            limit=1000,
            filter=MessagesFilter.VIDEO,
        ):
            results.append(f"{movie.video.file_id};{movie.caption};movie")
        for media in results:
            data = media.split(";", 2)
            similary = SequenceMatcher(None, search, data[1]).ratio()
            if similary >= 0.3:
                await msg.edit(
                    f"**__Yeehaw, I found the {data[2]} you asked for...__**"
                )
                await sleep(2)
                await msg.edit("\U0001f4be **__Downloading...__**")
                if data[2] == "serie":
                    video = await assistant.download_media(
                        data[0],
                        file_name=serie_name,
                        progress=progress,
                        progress_args=(client, message.chat, msg),
                    )
                if data[2] == "movie":
                    video = await assistant.download_media(
                        data[0],
                        file_name=movie_name,
                        progress=progress,
                        progress_args=(client, message.chat, msg),
                    )
                if VOICE_CHATS.get(message.chat.id) is None:
                    await msg.edit(
                        "\U0001fa84 **__Joining the voice chat...__**"
                    )
                    await on_call.join(message.chat.id)
                    VOICE_CHATS[message.chat.id] = on_call
                await sleep(1)
                await on_call.start_video(
                    video,
                    enable_experimental_lip_sync=True,
                    repeat=False,
                    with_audio=True,
                )
                await msg.edit(f"**__Streaming {data[2].upper()}__**")
                await msg.pin()
                break

            await msg.edit(
                "**__The request has not been found in our database, please try another name__**"
            )
            break
    except Exception as e:
        logging.error(e)
        await msg.edit(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
        if message.chat.id in VOICE_CHATS:
            await VOICE_CHATS[message.chat.id].stop()
            await clear_queue(message.chat)
            VOICE_CHATS.pop(message.chat.id)
