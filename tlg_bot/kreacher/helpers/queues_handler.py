from kreacher.dicts.dicts import VOICE_CHATS
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from kreacher.helpers.queues import (
    QUEUE,
    clear_queue,
    get_queue,
    pop_an_item,
    active,
)


async def skip_current(chat):
    if chat.id not in QUEUE:
        return 0
    chat_queue = get_queue(chat.id)
    if len(chat_queue) == 1:
        await VOICE_CHATS[chat.id].leave_group_call(chat.id)
        clear_queue(chat.id)
        active.remove(chat.id)
        return 1
    songname = chat_queue[1][0]
    url = chat_queue[1][1]
    link = chat_queue[1][2]
    type = chat_queue[1][3]
    RESOLUSI = chat_queue[1][4]
    if type == "Audio":
        await VOICE_CHATS[chat.id].change_stream(
            chat.id,
            AudioPiped(
                url,
            ),
        )
    elif type == "Video":
        if RESOLUSI == 720:
            hm = HighQualityVideo()
        elif RESOLUSI == 480:
            hm = MediumQualityVideo()
        elif RESOLUSI == 360:
            hm = LowQualityVideo()
        await VOICE_CHATS[chat.id].change_stream(
            chat.id, AudioVideoPiped(url, HighQualityAudio(), hm)
        )
    pop_an_item(chat.id)
    return [songname, link, type]


async def skip_item(chat_id: int, x: int):
    if chat_id not in QUEUE:
        return 0
    chat_queue = get_queue(chat_id)
    try:
        songname = chat_queue[x][0]
        chat_queue.pop(x)
        return songname
    except Exception as e:
        print(e)
        return 0
