import asyncio
from pyrogram import idle
from datetime import datetime
from termcolor import colored
from pyrogram.types import BotCommand

from bot.setup import setup_db, setup_plugins
from bot import kreacher, assistant

ay = asyncio.get_event_loop()


async def start_bot():
    print(f'{colored("[INFO]", "blue")}: LOADING BOT DETAILS')
    bot_me = await kreacher.get_me()
    print(f'{colored("[INFO]", "blue")}: BOT ID {bot_me.id}')
    await kreacher.set_bot_commands(
        commands=[
            BotCommand("config", "Set bot configuration"),
            BotCommand("help", "How to use this one"),
            BotCommand("leave", "Leave the voice chat"),
            BotCommand("ping", "Check server latency"),
            BotCommand("play_book", "Play pdf file as audiobook"),
            BotCommand("play_song", "Play audio in voice chat"),
            BotCommand("play_video", "Play video in voice chat"),
            BotCommand("speedtest", "Run server speed test"),
            BotCommand("streaming", "Any movie or series"),
        ]
    )
    print(f'{colored("[INFO]", "blue")}: SETED BOT COMMANDS')


setup_db()
setup_plugins()
ay.run_until_complete(start_bot())

print(f'{colored("[INFO]", "blue")}: SUCCESSFULLY STARTED BOT!')

START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def execution_time(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{}{}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


if __name__ == "__main__":
    try:
        idle()
    except KeyboardInterrupt:
        pass
    finally:
        kreacher.disconnect()
        assistant.disconnect()
        print(f'{colored("[INFO]", "blue")}: CLIENTS DISCONNECTED')
