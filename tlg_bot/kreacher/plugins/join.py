from kreacher import  call_py, client
from telethon import events


@client.on(events.NewMessage(pattern="[!?/]join"))
async def join_handler(event):
    chat = await event.get_chat()
    await call_py.start(chat.id)
