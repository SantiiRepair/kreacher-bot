import asyncio
from pyrogram import idle
from termcolor import colored
from pyrogram.types import BotCommand

from bot.setup import setup_plugins
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


try:
    setup_plugins()
    ay.run_until_complete(start_bot())
    print(f'{colored("[INFO]", "blue")}: SUCCESSFULLY STARTED BOT!')
    idle()
except KeyboardInterrupt:
    kreacher.disconnect()
    assistant.disconnect()
    print(f'{colored("[INFO]", "blue")}: CLIENTS DISCONNECTED')
