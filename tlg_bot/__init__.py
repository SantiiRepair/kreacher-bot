import os
import logging
from termcolor import colored
from tlg_bot.config import Config
from telethon.sync import TelegramClient
from pytgcalls import GroupCallFactory

config = Config()
dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(dir, "logs/logs.txt")
if os.path.exists(path) is False:
    with open(path, "w"):
        print(f'{colored("[INFO]", "blue")}: LOG FILE CREATED')

logging.basicConfig(
    filename=path,
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
ins = _factory.get_group_call()
client.start()
kreacher.start(bot_token=config.BOT_TOKEN)
