import logging
import functools
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.types import CallbackQuery
from pyrogram.enums.chat_type import ChatType


def only_admin_and_requester(func):
    """Allow only admins and user requester to use any command"""

    @functools.wraps(func)
    async def _(client: Client, anything):
        try:
            if isinstance(anything, Message):
                if not anything.chat.type == ChatType.PRIVATE:
                    user = await client.get_chat_member(
                        anything.chat.id, anything.from_user.id
                    )
                    if not user.privileges:
                        return await anything.reply(
                            "**__You are not my master, you do not order me what to do, bye__** \U0001f621"
                        )

            elif isinstance(anything, CallbackQuery):
                if not anything.message.chat.type == ChatType.PRIVATE:
                    user = await client.get_chat_member(
                        anything.message.chat.id, anything.message.from_user.id
                    )
                    if not user.privileges:
                        return await client.answer_callback_query(
                            anything.id,
                            text="**__You are not my master or played user, you cannot execute this action.__** \U0001f621",
                            show_alert=True,
                        )
            await func(client, anything)
        except Exception as err:
            logging.error(err)

    return _
