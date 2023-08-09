import asyncio
import pyrogram
from bot import kreacher, user
from bot.utils import loader
from termcolor import colored


async def start_bot():
    await loader()
    print(f'{colored("[INFO]", "blue")}: LOADING ASSISTANT DETAILS')
    bot_me = await kreacher.get_me()
    print(f'{colored("[INFO]", "blue")}: ASSISTANT ID {bot_me.id}')


loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())

print(f'{colored("[INFO]", "blue")}: SUCCESSFULLY STARTED BOT!')


if __name__ == "__main__":
    try:
        pyrogram.idle()
    except KeyboardInterrupt:
        kreacher.disconnect()
        user.disconnect()
        print(f'{colored("[INFO]", "blue")}: CLIENTS DISCONNECTED')
