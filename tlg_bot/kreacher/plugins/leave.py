from kreacher import call_py, kreacher
from telethon import events


@kreacher.on(events.NewMessage(pattern="[!?/]leave"))
async def leave_handler(event):
    await call_py.leave_current_group_call()
