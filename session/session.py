import os
from pyrogram import Client
from dotenv import load_dotenv


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, "../.env")
    load_dotenv(path)

    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")

    app = Client(":memory:", api_id=api_id, api_hash=api_hash)
    with app:
        print(app.export_session_string())
