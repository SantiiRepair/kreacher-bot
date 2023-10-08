import os
import logging
from redis import Redis
from pyrogram import Client
from termcolor import colored
from bot.config import config
from pytgcalls import GroupCallFactory
from bot.utils.driver import get_driver

_logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
_logs_file = os.path.join(_logs_dir, "kreacher.log")
if not os.path.exists(_logs_dir):
    os.makedirs(_logs_dir)
if os.path.exists(_logs_file) and os.stat(_logs_file).st_size > 0:
    with open(_logs_file, "w") as f:
        f.truncate(0)
        print(f'{colored("[INFO]", "blue")}: LOG FILE WAS FLUSHED SUCCESSFULLY')
elif not os.path.exists(_logs_file):
    try:
        with open(_logs_file, "w") as f:
            f.write("")
        print(f'{colored("[INFO]", "blue")}: LOG FILE CREATED')
    except Exception as e:
        logging.error(e)


logging.basicConfig(
    filename=_logs_file,
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

BOT_USERNAME = config.BOT_USERNAME

# Bot Client
kreacher = Client(
    "bot.kreacher",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

# UserBot Client
assistant = Client(
    "userbot.assistant",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.SESSION_STRING,
)

r = Redis(
    host="localhost",
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD,
)

on_call = GroupCallFactory(
    assistant, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM
).get_group_call()
kreacher.start()
assistant.start()
driver = get_driver()
