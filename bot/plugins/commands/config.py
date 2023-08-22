import os
from tinydb import TinyDB, Query
from pyrogram.types import Message
from bot import assistant, kreacher
from pyrogram import filters, Client
from bot.decorators.only_admins import only_admins
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

c = os.path.dirname(os.path.abspath(__file__))


@kreacher.on_message(filters.regex(pattern="^[!?/]config"))
@only_admins
async def _(client: Client, message: Message):
    registry = os.path.join(c, "../dbs/registry.json")
    db = TinyDB(registry)
    groups = db.table("groups")
    user = groups.search(Query().id == message.chat.id)
    common = await assistant.get
    if len(common) > 0:
        print(common)
