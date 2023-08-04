from kreacher import call_py, kreacher
from telethon import events


@kreacher.on(events.callbackquery.CallbackQuery(data="cls"))
async def _(event):
    await event.delete()


@kreacher.on(events.callbackquery.CallbackQuery(data="pause_callback"))
async def _(event):
    await call_py.set_pause(True)


@kreacher.on(events.callbackquery.CallbackQuery(data="resume_callback"))
async def _(event):
    await call_py.set_pause(False)


@kreacher.on(events.callbackquery.CallbackQuery(data="end_callback"))
async def _(event):
    await call_py.stop_media()
