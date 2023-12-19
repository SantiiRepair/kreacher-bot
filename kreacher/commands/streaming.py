import uuid
import logging
from asyncio import sleep
from bot.config import config
from pyrogram.types import Message
from difflib import SequenceMatcher
from pyrogram import filters, Client
from pyrogram.enums import MessagesFilter
from bot.helpers.progress import progress
from bot.scrapers.images import ImageScraper
from bot import userbot, kreacher, tgcalls, VOICE_CHATS
from bot.decorators.sides import only_groups_or_channels
from bot.helpers.queues import (
    remove_queue,
)


@kreacher.on_message(filters.regex(pattern="^[!?/]streaming"))
@only_groups_or_channels
async def _(client: Client, message: Message):
    results = []
    try:
        if " " not in message.text:
            return await message.reply(
                "**__How to use this command.\n\nNext we show two ways to use this command, click on the button with the mode you are looking for to know details.__**"
            )
        _message = await message.reply("🔎 **__Searching...__**")
        await sleep(2)
        search = message.text.split(maxsplit=1)[1]
        series_channel = await userbot.get_chat(config.ES_SERIES_CHANNEL)
        movies_channel = await userbot.get_chat(config.ES_MOVIES_CHANNEL)
        async for serie in userbot.search_messages(
            chat_id=series_channel.id,
            query=search,
            limit=1000,
            filter=MessagesFilter.VIDEO,
        ):
            results.append(
                {
                    "type": "serie",
                    "caption": serie.caption,
                    "file_id": serie.video.file_id,
                }
            )
        async for movie in userbot.search_messages(
            chat_id=movies_channel.id,
            query=search,
            limit=1000,
            filter=MessagesFilter.VIDEO,
        ):
            results.append(
                {
                    "type": "movie",
                    "caption": movie.caption,
                    "file_id": movie.video.file_id,
                }
            )
        for media in results:
            similary = SequenceMatcher(None, search, media["caption"]).ratio()
            if similary >= 0.3:
                await _message.edit(
                    f"**__I found the {media['type']} you asked for...__**"
                )
                await sleep(2)
                await _message.edit("💾 **__Downloading...__**")
                image_scraper = ImageScraper(
                    "/tmp", search_key=f"{media['caption']} poster"
                )
                image_urls = image_scraper.find_image_urls()
                photo = image_scraper.save_images(image_urls, keep_filenames=True)
                mime_type = (
                    message.reply_to_message.video.mime_type.split("/", 1)[1]
                    if message.reply_to_message.video
                    else message.reply_to_message.file.mime_type.split("/", 1)[1]
                )
                file_name = f"/tmp/{str(uuid.uuid4())}.{mime_type}"
                video = await userbot.download_media(
                    media["file_id"],
                    file_name=file_name,
                    progress=progress,
                    progress_args=(client, message.chat.id, _message.id),
                )
                if VOICE_CHATS.get(message.chat.id) is None:
                    await _message.edit("🪄 **__Joining the voice chat...__**")
                    VOICE_CHATS[message.chat.id] = tgcalls.get_group_call()
                    await VOICE_CHATS[message.chat.id].start(message.chat.id)
                await sleep(2)
                await VOICE_CHATS[message.chat.id].start_video(
                    video,
                    enable_experimental_lip_sync=True,
                    repeat=False,
                )
                await _message.delete()
                await client.send_photo(
                    message.chat.id,
                    photo=photo,
                    caption=f"**__Streaming {media['type'].upper()}__**",
                )
                await _message.pin()
                break

            await _message.edit(
                "**__The request has not been found in our database, please try another name__**"
            )
            break
    except Exception as err:
        logging.error(err)
        await _message.edit(
            f"**__Oops master, something wrong has happened.__** \n\n`Error: {err}`",
        )
        if message.chat.id in VOICE_CHATS:
            await VOICE_CHATS[message.chat.id].stop()
            remove_queue(str(message.chat.id))
            VOICE_CHATS.pop(message.chat.id)
