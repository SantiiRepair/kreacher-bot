import os
from dotenv import load_dotenv


class Config(object):
    def __init__(self):
        cwd = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(cwd, "../.env")
        load_dotenv(path)

        self.API_ID = os.getenv("API_ID")
        self.API_HASH = os.getenv("API_HASH")
        self.BOT_TOKEN = os.getenv("BOT_TOKEN")
        self.BOT_USERNAME = os.getenv("BOT_USERNAME")
        self.CHANNEL = os.getenv("CHANNEL")
        self.ES_MOVIES_CHANNEL = os.getenv("ES_MOVIES_CHANNEL")
        self.ES_SERIES_CHANNEL = os.getenv("ES_SERIES_CHANNEL")
        self.MANAGEMENT_MODE = os.getenv("MANAGEMENT_MODE")
        self.MANTAINER = os.getenv("MANTAINER")
        self.SESSION_STRING = os.getenv("SESSION_STRING")
        self.POSTGRES_DB = os.getenv("POSTGRES_DB")
        self.POSTGRES_USER = os.getenv("POSTGRES_USER")
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST")
        self.POSTGRES_PORT = os.getenv("POSTGRES_PORT")
        self.REDIS_HOST = os.getenv("REDIS_HOST")
        self.REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
        self.REDIS_PORT = os.getenv("REDIS_PORT")


config = Config()
