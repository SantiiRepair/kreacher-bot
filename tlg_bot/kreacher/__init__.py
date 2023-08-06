from config import Config
from telethon.sync import TelegramClient
import logging
from pytgcalls import GroupCallFactory

config = Config()
logging.basicConfig(
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
