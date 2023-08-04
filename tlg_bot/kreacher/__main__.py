import asyncio
import telethon
import glob
from pathlib import Path
from kreacher.utils import load_plugins
import logging
from termcolor import colored
from kreacher import kreacher
from kreacher import client


logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

path = "kreacher/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))


async def start_bot():
    print(f'{colored("[INFO]", "blue")}: LOADING ASSISTANT DETAILS')
    botme = await client.get_me()
    botid = telethon.utils.get_peer_id(botme)
    print(f'{colored("[INFO]", "blue")}: ASSISTANT ID {botid}')


loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())

print(f'{colored("[INFO]", "blue")}: SUCCESSFULLY STARTED BOT!')


if __name__ == "__main__":
    kreacher.run_until_disconnected()
