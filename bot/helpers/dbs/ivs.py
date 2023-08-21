import os
import uuid
from tinydb import TinyDB
from datetime import datetime
from pyrogram.types import Message
from bot.helpers.user_info import user_info

current_dir = os.path.dirname(os.path.abspath(__file__))


async def new_invoice(message: Message, net: str, sub_type: str):
    registry = os.path.join(current_dir, "../dbs/registry.json")
    db = TinyDB(registry)
    ivs = db.table("invoices")
    txs = db.table("transactions")
    user = await user_info(message.from_user)
    match net:
        case "tron":
            ivs.insert(
                {
                    "id": str(uuid.uuid4()),
                    "date": str(datetime.utcnow()).split(" ", 1)[0],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "subscription": sub_type,
                    "userId": message.from_user.id,
                }
            )

        case "ethereum":
            ivs.insert(
                {
                    "id": str(uuid.uuid4()),
                    "date": str(datetime.utcnow()).split(" ", 1)[0],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "subscription": sub_type,
                    "userId": message.from_user.id,
                }
            )
