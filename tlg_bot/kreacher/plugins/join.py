from kreacher import  call_py, kreacher
from telethon import events


@kreache.on(events.NewMessage(pattern="[!?/]join"))
async def join_handler(event):
    chat = await event.get_chat()
    await call_py.start(chat.id)
