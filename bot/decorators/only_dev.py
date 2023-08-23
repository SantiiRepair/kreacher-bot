import functools
from bot import config
from pyrogram import Client
from pyrogram.types import Message


def only_dev(func):
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
