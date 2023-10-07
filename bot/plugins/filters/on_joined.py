"""
import os
from bot import kreacher
from tinydb import TinyDB, Query
from pyrogram.types import Message
from pyrogram import filters, Client

c = os.path.dirname(os.path.abspath(__file__))


@kreacher.on_message(filters.new_chat_members)
async def _(client: Client, message: Message):
    registry = os.path.join(c, "../../dbs/registry.json")
    db = TinyDB(registry)
    groups = db.table("groups")
    bot_me = await client.get_me()
    if message.new_chat_members and bot_me.id in [
        user.id for user in message.new_chat_members
    ]:
        if not bool(groups.search(Query().id == message.chat.id)):
            await client.send_message(
                message.chat.id,
                "**__Whoops!\n\nYou can't use me without a subscription__**",
            )
            return await client.leave_chat(message.chat.id)
        groups.insert(
            {
                "id": message.chat.id,
                "group_name": message.chat.title,
                "subscription": None,
            }
        )
"""