import os
import asyncio
import telethon
import glob
from pathlib import Path
from bot.utils import loader
import logging
from termcolor import colored
from bot import kreacher


logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

path = "bot/plugins/*.py"
files = glob.glob(path)
for file in files:
    with open(file) as a:
        patt = Path(a.name)
        name = patt.stem
        loader(name.replace(".py", ""))


async def start_bot():
    print(f'{colored("[INFO]", "blue")}: LOADING ASSISTANT DETAILS')
    botme = await kreacher.get_me()
    botid = telethon.utils.get_peer_id(botme)
    print(f'{colored("[INFO]", "blue")}: ASSISTANT ID {botid}')


loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())

print(f'{colored("[INFO]", "blue")}: SUCCESSFULLY STARTED BOT!')


if __name__ == "__main__":
    kreacher.run_until_disconnected()
