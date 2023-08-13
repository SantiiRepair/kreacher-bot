import asyncio
import pyrogram
from bot import kreacher, assistant
from bot.utils import loader
from termcolor import colored
from pyrogram.types import BotCommand


async def start_bot():
    await loader()
    print(f'{colored("[INFO]", "blue")}: LOADING BOT DETAILS')
    bot_me = await kreacher.get_me()
    print(f'{colored("[INFO]", "blue")}: BOT ID {bot_me.id}')
    await kreacher.set_bot_commands(
        commands=[
            BotCommand("config", "Set bot configuration"),
            BotCommand("join", "Join the voice chat"),
            BotCommand("leave", "Leave the voice chat"),
            BotCommand("me", "Info about your status"),
            BotCommand("ping", "Check server latency"),
            BotCommand("play_song", "Play audio in voice chat"),
            BotCommand("play_video", "Play video in voice chat"),
            BotCommand("speedtest", "Run server speed test"),
            BotCommand("streaming", "Any movie or series"),
        ]
    )
    print(f'{colored("[INFO]", "blue")}: SETED BOT COMMANDS')


loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())

print(f'{colored("[INFO]", "blue")}: SUCCESSFULLY STARTED BOT!')


if __name__ == "__main__":
    try:
        pyrogram.idle()
    except KeyboardInterrupt:
        kreacher.disconnect()
        assistant.disconnect()
        print(f'{colored("[INFO]", "blue")}: CLIENTS DISCONNECTED')
