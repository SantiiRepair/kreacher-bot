from Config import Config
from kreacher import client, kreacher
from telethon import events
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterVideo
import tempfile
import uuid

query = "ejemplo"


@kreacher.on(events.NewMessage(chats=Config().MOVIES_CHANNEL))
async def find_movie(event, q):
    messages = await client(
        SearchRequest(
            peer=Config().MOVIES_CHANNEL,
            q=q,
            filter=InputMessagesFilterVideo(),
            max_id=0,
            min_id=0,
            add_offset=0,
            limit=100,
            min_date=None,
            max_date=None,
            hash=0,
        )
    )

    if messages.total > 0:
        video_message = messages.messages[0]

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            await client.download_media(video_message.video, temp_file)
            video_path = temp_file.name

        file_name = f"{uuid.uuid4()}.mp4"
        with open(file_name, "wb") as f:
            with open(video_path, "rb") as f2:
                f.write(f2.read())
