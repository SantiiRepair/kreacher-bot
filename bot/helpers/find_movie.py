import uuid
import tempfile
from bot import kreacher
from bot.config import config


query = "ejemplo"


@kreacher.on(events.NewMessage(chats=config.MOVIES_CHANNEL))
async def find_movie(message, q):
    messages = await kreacher(
        SearchRequest(
            peer=config.MOVIES_CHANNEL,
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
            await kreacher.download_media(video_message.video, temp_file)
            video_path = temp_file.name

        file_name = f"{uuid.uuid4()}.mp4"
        with open(file_name, "wb") as f:
            with open(video_path, "rb") as f2:
                f.write(f2.read())
