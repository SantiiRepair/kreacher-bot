import os
from bot import kreacher
from pyrogram import filters, Client
from pyrogram.types import Message
from tinydb import TinyDB, Query
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

current_dir = os.path.dirname(os.path.abspath(__file__))


@kreacher.on_message(filters.regex(pattern="^[!?/]config"))
async def _(client: Client, message: Message):
    registry = os.path.join(current_dir, "../dbs/registry.json")
    db = TinyDB(registry)
    chats = db.table("chats")
    user = chats.search(Query().id == message.from_user.id)
    if not user:
        return await message.reply(
            "**__Mr. Wizard, send me a private message to save your info__** \U0001f52e"
        )
    document = os.path.join(
        current_dir, f"../downloads/photos/{user[0]['id']}.png"
    )
    caption = f"**ID**: `{user[0]['id']}`\n\n**Name**: [{user[0]['first_name']}]({user[0]['linked']})\n**Alias**: {user[0]['username']}\n**Subscription**: {user[0]['subscription']}\n**Since**: {user[0]['since']}"
    reply_markup = (
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "\U0001f4e2 ᴄʜᴀɴɴᴇʟ",
                        url="https://t.me/KreacherStreamerChannel",
                    )
                ]
            ]
        )
        if user[0]["subscription"]
        else InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "\U0001f4b3 ɴᴏʀᴍᴀʟ", callback_data="normal"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "\U0001f4b3 ᴘʀᴇᴍɪᴜᴍ", callback_data="premium"
                    )
                ],
            ]
        )
    )
    await kreacher.download_media(user[0]["photo"], file_name=document)
    await message.reply_document(
        document=document,
        caption=caption,
        reply_markup=reply_markup,
    )
    os.remove(document)


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
            return await client.leave_chat(message.chat.id)
