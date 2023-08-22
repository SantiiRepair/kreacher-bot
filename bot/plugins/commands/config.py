import os
from tinydb import TinyDB, Query
from pyrogram.types import Message
from bot import assistant, kreacher
from pyrogram import filters, Client
from bot.decorators.only_admins import only_admins
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

current_dir = os.path.dirname(os.path.abspath(__file__))


@kreacher.on_message(filters.regex(pattern="^[!?/]config"))
@only_admins
async def _(client: Client, message: Message):
    registry = os.path.join(current_dir, "../dbs/registry.json")
    db = TinyDB(registry)
    groups = db.table("groups")
    user = groups.search(Query().id == message.chat.id)
    common = await assistant.get
    if len(common) > 0:
        print(common)


@kreacher.on_message(filters.new_chat_members)
async def _(client: Client, message: Message):
    registry = os.path.join(current_dir, "../dbs/registry.json")
    db = TinyDB(registry)
    groups = db.table("groups")
    bot_me = await client.get_me()
    if message.new_chat_members and bot_me.id in [
        user.id for user in message.new_chat_members
    ]:
        if not bool(groups.search(Query().id == str(message.chat.id))):
            await client.send_message(
                message.chat.id,
                "**__Whoops!\n\nYou can't use me without a subscription__**",
            )
            await client.leave_chat(message.chat.id)
