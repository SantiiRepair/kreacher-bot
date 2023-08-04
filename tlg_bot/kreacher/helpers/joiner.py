from kreacher import kreacher, call_py
from telethon import events


@kreacher.on(events.NewMessage(outgoing=True, pattern="^[?!/]join"))
async def join_handler(event):
    chat = await event.get_chat()
    await call_py.start(chat.id)
