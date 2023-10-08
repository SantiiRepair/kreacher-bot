import logging
import functools
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.types import CallbackQuery
from pyrogram.enums.chat_type import ChatType


def only_managers(func):
    """
    Allow only admins and user requester to use any command.
    """

    @functools.wraps(func)
    async def _(client: Client, any):
        try:
            if isinstance(any, Message):
                if not any.chat.type == ChatType.PRIVATE:
                    user = await client.get_chat_member(any.chat.id, any.from_user.id)
                    if not user.privileges:
                        return await any.reply(
                            "**__You are not my master, you do not order me what to do, bye__** \U0001f621"
                        )

            elif isinstance(any, CallbackQuery):
                if not any.message.chat.type == ChatType.PRIVATE:
                    user = await client.get_chat_member(
                        any.message.chat.id, any.message.from_user.id
                    )
                    if not user.privileges:
                        return await client.answer_callback_query(
                            any.id,
                            text="**__You are not my master or played user, you cannot execute this action.__** \U0001f621",
                            show_alert=True,
                        )
            await func(client, any)
        except Exception as e:
            logging.error(e)

    return _
