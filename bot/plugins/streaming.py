import os
import uuid
from pyrogram import filters
from bot import assistant, kreacher
from bot.helpers.progress import progress
from pyrogram.enums import MessagesFilter

query = "ejemplo"
current_dir = os.path.dirname(os.path.abspath(__file__))


@kreacher.on_message(filters.regex(pattern="^[!?/]streaming"))
async def _(client, message):
    try:
        msg = await message.reply("**__Searching...__**")
        channel_username = "corpoelec"
        search_text = "The Witcher"
        download_as = os.path.join(
            current_dir, f"../downloads/videos/{str(uuid.uuid4())}.mp4"
        )
        channel_info = await assistant.get_chat("-1001929383972")

        async for m in assistant.search_messages(
            chat_id=channel_info.id, query=search_text, limit=200, filter=MessagesFilter.VIDEO
        ):
            if m.video and search_text.lower() in m.caption.lower():
                print(m.caption)
                await assistant.download_media(
                    m.video.file_id,
                    file_name=download_as,
                    progress=progress,
                    progress_args=(client, message.chat, msg),
                )
                print("Video descargado exitosamente.")
                break

        else:
            print(
                "No se encontró ningún mensaje con el texto buscado o no contiene un video."
            )

    except Exception as e:
        print(e)
