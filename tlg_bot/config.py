import os
from dotenv import find_dotenv, load_dotenv


class Config(object):
    def __init__(self):
        load_dotenv(find_dotenv())
        print(os.getenv("API_HASH"))
        self.API_HASH = os.getenv("API_HASH")
        self.API_ID = os.getenv("API_ID")
        self.ASSISTANT_ID = os.getenv("ASSISTANT_ID")
        self.AUTO_LEAVE = os.getenv("AUTO_LEAVING_ASSISTANT")
        self.AUTO_LEAVE_TIME = os.getenv("AUTO_LEAVE_ASSISTANT_TIME")
        self.BOT_OWNER = os.getenv("BOT_OWNER")
        self.BOT_TOKEN = os.getenv("BOT_TOKEN")
        self.BOT_USERNAME = os.getenv("BOT_USERNAME")
        self.CHANNEL = os.getenv("CHANNEL")
        self.CMD_IMG = os.getenv("CMD_IMG")
        self.HEROKU_MODE = os.getenv("HEROKU_MODE")
        self.MANAGEMENT_MODE = os.getenv("MANAGEMENT_MODE")
        self.MOVIES_CHANNEL = os.getenv("MOVIES_CHANNEL")
        self.START_IMG = os.getenv("START_IMG")
        self.SUPPORT = os.getenv("SUPPORT")
