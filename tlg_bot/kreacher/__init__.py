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

_bot = TelegramClient(None, api_id=config.API_ID, api_hash=config.API_HASH)
kreacher = _bot.start(bot_token=config.BOT_TOKEN)
client = TelegramClient(None, config.API_ID, config.API_HASH)
client.start()
