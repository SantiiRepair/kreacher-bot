import logging
import functools
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums.chat_type import ChatType


def only_admins(func):
    """Allow only admins to use any command"""

    @functools.wraps(func)
    async def _(client: Client, message: Message):
        if not message.chat.type == ChatType.PRIVATE:
            try:
                user = await client.get_chat_member(
                    message.chat.id, message.from_user.id
                )
                if not user.privileges:
                    return await message.reply(
                        "**__You are not my master, you do not order me what to do, bye__** \U0001f621"
                    )
            except Exception as e:
                logging.error(e)
        await func(client, message)

    return _
