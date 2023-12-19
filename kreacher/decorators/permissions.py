import logging
import functools
from bot import config
from pyrogram import Client
from pyrogram.enums.chat_type import ChatType
from pyrogram.types import Message, CallbackQuery


def only_dev(func):
    """Allow only dev to use any command"""

    @functools.wraps(func)
    async def _(client: Client, message: Message):
        dev = await client.get_users(config.MANTAINER)
        if not dev.id == message.from_user.id:
            return await message.reply(
                f"**__Only [{dev.first_name}](https://t.me/{dev.username}), can execute this command__** \U0001f6ab",
                disable_web_page_preview=True,
            )
        await func(client, message)

    return _


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
            except Exception as err:
                logging.error(err)
        await func(client, message)

    return _


def only_admins_or_requester(func):
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
