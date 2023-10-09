import asyncio
from pyrogram import idle
from termcolor import colored
from pyrogram.types import BotCommand

from bot.util import setup_db, setup_plugins
from bot import kreacher, assistant


async def start_bot():
    print(f'{colored("[INFO]", "blue")}: LOADING BOT DETAILS')
    bot_me = await kreacher.get_me()
    print(f'{colored("[INFO]", "blue")}: BOT ID {bot_me.id}')
    await kreacher.set_bot_commands(
        commands=[
            BotCommand("config", "Set bot configuration"),
            BotCommand("help", "How to use this one"),
            BotCommand("leave", "Leave the voice chat"),
            BotCommand("me", "Info about your status"),
            BotCommand("ping", "Check server latency"),
            BotCommand("play_book", "Play pdf file as audiobook"),
            BotCommand("play_song", "Play audio in voice chat"),
            BotCommand("play_video", "Play video in voice chat"),
            BotCommand("speedtest", "Run server speed test"),
            BotCommand("streaming", "Any movie or series"),
        ]
    )
    print(f'{colored("[INFO]", "blue")}: SETED BOT COMMANDS')


ay = asyncio.get_event_loop()
ay.run_until_complete(setup_db())
ay.run_until_complete(setup_plugins())
ay.run_until_complete(start_bot())

print(f'{colored("[INFO]", "blue")}: SUCCESSFULLY STARTED BOT!')


if __name__ == "__main__":
    try:
        idle()
    except KeyboardInterrupt:
        pass
    finally:
        kreacher.disconnect()
        assistant.disconnect()
        print(f'{colored("[INFO]", "blue")}: CLIENTS DISCONNECTED')
