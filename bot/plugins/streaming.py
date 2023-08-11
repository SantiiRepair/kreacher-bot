import os
import uuid
from asyncio import sleep
import logging
from pyrogram import filters
from bot import assistant, kreacher, on_call
from bot.config import config
from bot.helpers.progress import progress
from pyrogram.enums import MessagesFilter
from bot.instance_of.every_vc import VOICE_CHATS
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

            if "capitulo" in search or "episodio" in search.lower():
                series_channel = await assistant.get_chat(
                    config.ES_SERIES_CHANNEL
                )
                print(series_channel)
                # limit = movies_channel["message_count"]
                async for media in assistant.search_messages(
                    chat_id=series_channel.id,
                    query=search,
                    limit=1000,
                    filter=MessagesFilter.VIDEO,
                ):
                    if media.video and search.lower() in media.caption.lower():
                        await msg.edit(
                            " **__Yeehaw, I found the serie you asked for...__**"
                        )
                        await sleep(2)
                        await msg.edit("\U0001f4be **__Downloading...__**")
                        serie_file = await assistant.download_media(
                            media.video.file_id,
                            file_name=movie,
                            progress=progress,
                            progress_args=(client, chat, msg),
                        )
                        await join(chat.id)
                        return await on_call.start_video(
                            serie_file, repeat=False
                        )
                        break

                    else:
                        return await msg.edit(
                            "**__The request has not been found in our database, please try another name__**"
                        )
            else:
                movies_channel = await assistant.get_chat(
                    config.ES_MOVIES_CHANNEL
                )
                # limit = movies_channel["message_count"]
                async for media in assistant.search_messages(
                    chat_id=movies_channel.id,
                    query=search,
                    limit=1000,
                    filter=MessagesFilter.VIDEO,
                ):
                    if media.video and search.lower() in media.caption.lower():
                        await msg.edit(
                            " **__Yeehaw, I found the movie you asked for...__**"
                        )
                        await sleep(2)
                        await msg.edit("\U0001f4be **__Downloading...__**")
                        movie_file = await assistant.download_media(
                            media.video.file_id,
                            file_name=movie,
                            progress=progress,
                            progress_args=(client, chat, msg),
                        )
                        await on_call.join(chat.id)
                        await on_call.start_video(movie_file, repeat=False)
                        return await msg.edit("**__Streaming Movie**__")
                        break

                else:
                    return await msg.edit(
                        "**__The request has not been found in our database, please try another name__**"
                    )
    except Exception as e:
        logging.error(e)
        await msg.edit(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {e}`",
        )
        if chat.id in VOICE_CHATS:
            await VOICE_CHATS[chat.id].stop()
            await clear_queue(chat)
            VOICE_CHATS.pop(chat.id)
