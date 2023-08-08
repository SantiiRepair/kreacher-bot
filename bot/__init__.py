import os
import asyncio
import logging
from termcolor import colored
from bot.config import config
from telethon.sync import TelegramClient
from pytgcalls import GroupCallFactory


dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(dir, "logs/logs.txt")
def logs():
    if os.path.exists(path):
        pass
    else:
        try:
            with open(ruta_archivo, 'w') as g:
                f.write('')
            print(f'{colored("[INFO]", "blue")}: LOG FILE CREATED')
        except Exception as e:
            print(e)


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
on_call = _factory.get_group_call()
client.start()
kreacher.start(bot_token=config.BOT_TOKEN)
