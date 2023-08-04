from telethon import events, Button
from kreacher import kreacher
from kreacher.status import *


@kreacher.on(events.callbackquery.CallbackQuery(data="admin"))
async def _(event):
    await event.edit(
        ADMIN_TEXT, buttons=[[Button.inline("« Bᴀᴄᴋ", data="help")]]
    )


@kreacher.on(events.callbackquery.CallbackQuery(data="play"))
async def _(event):
    await event.edit(
        PLAY_TEXT, buttons=[[Button.inline("« Bᴀᴄᴋ", data="help")]]
    )


ADMIN_TEXT = """
**✘ A module from which admins of the chat can use!**

‣ `/end` - To End music streaming.
‣ `/skip` - To Skip Tracks Going on.
‣ `/pause` - To Pause streaming.
‣ `/resume` - to Resume Streaming.
‣ `/leavevc` - force The Userbot to leave Vc Chat (Sometimes Joined).
‣ `/playlist` - to check playlists.
"""

PLAY_TEXT = """
**✘ A module from which users of the chat can use!**

‣ `/play` - To play audio from else reply to audio file.
‣ `/vplay` - To stream videos in voice chat.
"""
