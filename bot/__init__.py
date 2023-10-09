import os
import logging
from redis import Redis
import sqlalchemy as db
from pyrogram import Client
from termcolor import colored
from pytgcalls import GroupCallFactory

from bot.config import config
from bot.utils.driver import get_driver

# ------------------------------------------------------------------------------

VOICE_CHATS = {}

# ------------------------------------------------------------------------------

_API_ID = config.API_ID
_API_HASH = config.API_ID
_BOT_TOKEN = config.BOT_TOKEN
_SESSION_STRING = config.SESSION_STRING
_POSTGRES_DB = config.POSTGRES_DB
_POSTGRES_USER = config.POSTGRES_USER
_POSTGRES_PASSWORD = config.POSTGRES_PASSWORD
_POSTGRES_HOST = config.POSTGRES_HOST
_POSTGRES_PORT = config.POSTGRES_PORT
_REDIS_HOST = config.REDIS_HOST
_REDIS_PORT = config.REDIS_PORT
_REDIS_PASSWORD = config.REDIS_PASSWORD

# ------------------------------------------------------------------------------

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

# ------------------------------------------------------------------------------

logging.basicConfig(
    filename=_logs_file,
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

# ------------------------------------------------------------------------------

kreacher = Client(
    "bot.kreacher",
    api_id=_API_ID,
    api_hash=_API_HASH,
    bot_token=_BOT_TOKEN,
)

assistant = Client(
    "userbot.assistant",
    api_id=_API_ID,
    api_hash=_API_HASH,
    session_string=_SESSION_STRING,
)

# ------------------------------------------------------------------------------

engine = db.create_engine(
    f"postgresql://{_POSTGRES_USER}:{_POSTGRES_PASSWORD}@{_POSTGRES_HOST}:{_POSTGRES_PORT}/{_POSTGRES_DB}",
    echo=True,
)
conn = engine.connect()
db_metadata = db.MetaData()

# ------------------------------------------------------------------------------

r = Redis(
    host=_REDIS_HOST,
    port=_REDIS_PORT,
    password=_REDIS_PASSWORD,
)

# ------------------------------------------------------------------------------

on_call = GroupCallFactory(
    assistant, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM
).get_group_call()

# ------------------------------------------------------------------------------

kreacher.start()
assistant.start()
driver = get_driver()
