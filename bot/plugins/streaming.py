import os
import uuid
import asyncio
import logging
from pyrogram import filters
from bot import assistant, kreacher, on_call
from bot.config import config
from bot.helpers.progress import progress
from pyrogram.enums import MessagesFilter
from bot.helpers.queues import (
    add_to_queue,
    clear_queue,
)

current_dir = os.path.dirname(os.path.abspath(__file__))


@kreacher.on_message(filters.regex(pattern="^[!?/]streaming"))
async def _(client, message):
    chat = message.chat
    try:
        if not " " in message.text:
            return await message.reply(
                "**__How to use this command.\n\nNext we show two ways to use this command, click on the button with the mode you are looking for to know details.__**"
            )
        if " " in message.text:
            msg = await message.reply("**__Searching...__**")
            await sleep(2)
            search = message.text.split(maxsplit=1)[1]
            movie = os.path.join(
                current_dir, f"../downloads/movies/{str(uuid.uuid4())}.mp4"
            )
            serie = os.path.join(
                current_dir, f"../downloads/series/{str(uuid.uuid4())}.mp4"
            )

            if "capitulo" in search or "episodio" in search:
                series_channel = await assistant.get_chat(
                    config.ES_SERIES_CHANNEL
                )
                limit = await assistant.get()
                async for media in assistant.search_messages(
                    chat_id=movies_channel.id,
                    query=search,
                    limit=200,
                    filter=MessagesFilter.VIDEO,
                ):
                    if media.video and search.lower() in media.caption.lower():
                        await msg.edit("\U0001f4be **__Downloading...__**")
                        serie_file = await assistant.download_media(
                            media.video.file_id,
                            file_name=movie,
                            progress=progress,
                            progress_args=(client, chat, msg),
                        )
                        await on_call.start_video(serie_file, repeat=False)
                        break

                    else:
                        return await msg.edit("")
            else:
                movies_channel = await assistant.get_chat(
                    config.ES_MOVIES_CHANNEL
                )
                limit = await assistant.get()
                async for media in assistant.search_messages(
                    chat_id=movies_channel.id,
                    query=search,
                    limit=200,
                    filter=MessagesFilter.VIDEO,
                ):
                    if media.video and search.lower() in media.caption.lower():
                        await msg.edit("\U0001f4be **__Downloading...__**")
                        serie_file = await assistant.download_media(
                            media.video.file_id,
                            file_name=movie,
                            progress=progress,
                            progress_args=(client, chat, msg),
                        )
                        await on_call.start_video(serie_file, repeat=False)
                        break

                    else:
                        return await msg.edit("")
    except Exception as e:
        logging.error(e)
        await clear_queue(chat)
        await VOICE_CHATS[chat.id].stop()
        await msg.edit(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
        VOICE_CHATS.pop(chat.id)
