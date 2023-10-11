import sys
from pyrogram import Client


if __name__ == "__main__":
    try:
        api_id = input("Enter your Telegram API ID: ")
        api_hash = input("Enter your Telegram API HASH: ")

        app = Client(":memory:", api_id=api_id, api_hash=api_hash)
        with app:
            print(app.export_session_string())
    except KeyboardInterrupt:
        sys.exit(print("\n\nAborted!"))
