import functools
from bot import kreacher
from pyrogram.types import Message
from pyrogram.enums.chat_type import ChatType


def cmd_protected(func):
    @functools.wraps(func)
    async def _(message: Message):
        is_admin = False
        if not message.chat.type == ChatType.PRIVATE:
            try:
                _u = await kreacher.get_chat_member(
                    message.chat.id, message.from_user.id
                )
                if not _u.privileges:
                    is_admin = False
                    return await message.reply(
                        "**__You are not my master, you do not order me what to do, bye__** \U0001f621"
                    )
                is_admin = True
            except Exception:
                is_admin = False
        if is_admin:
            await func(message, _u)
        else:
            await message.reply(
                "**__You are not my master, you do not order me what to do, bye__** \U0001f621"
            )

    return _
