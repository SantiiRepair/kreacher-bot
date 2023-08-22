import logging
import functools
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums.chat_type import ChatType


def only_grps_chnns(func):
    @functools.wraps(func)
    async def _(client: Client, message: Message):
        if message.chat.type == ChatType.PRIVATE:
            return await message.reply(
            "**__Mr. Wizard, this command can only be used in groups or channels__** \U0001f937\U0001f3fb\u200D\u2642\uFE0F"
            )
        await func(client, message)
    return _
