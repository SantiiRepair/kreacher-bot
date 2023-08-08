import os
import logging
from termcolor import colored
from bot.config import config
from telethon.sync import TelegramClient
from pytgcalls import GroupCallFactory


dir = os.path.dirname(os.path.abspath(__file__))
folder = os.path.join(dir, "logs")

if not os.path.exists(folder):
    os.makedirs(folder)
if (
    os.path.exists(f"{folder}/logs.txt")
    and os.stat(f"{folder}/logs.txt").st_size > 0
):
    with open(f"{folder}/logs.txt", "w") as f:
        f.truncate(0)
        print(
            f'{colored("[INFO]", "blue")}: LOG FILE WAS FLUSHED SUCCESSFULLY'
        )
        f.close()
elif not os.path.exists(f"{folder}/logs.txt"):
    try:
        with open(f"{folder}/logs.txt", "w") as f:
            f.write("")
        print(f'{colored("[INFO]", "blue")}: LOG FILE CREATED')
    except Exception as e:
        logging.err(e)


logging.basicConfig(
    filename=f"{folder}/logs.txt",
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

BOT_USERNAME = config.BOT_USERNAME
ASSISTANT_ID = config.ASSISTANT_ID

client = TelegramClient(None, api_id=config.API_ID, api_hash=config.API_HASH)
kreacher = TelegramClient(None, api_id=config.API_ID, api_hash=config.API_HASH)
_factory = GroupCallFactory(
    client, GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON
)
on_call = _factory.get_group_call()
client.start()
kreacher.start(bot_token=config.BOT_TOKEN)
