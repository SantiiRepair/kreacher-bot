import os
import asyncio
import logging
from bot import kreacher
from termcolor import colored
from telethon.tl.types import InputPeerUser


async def send_log():
    dir = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(dir, "../logs/logs.txt")
    try:
        entity = await kreacher.get_entity()
        user = InputPeerUser(entity.id, entity.access_hash)
        await kreacher.send_file(user, file=file)
        print(f'{colored("[INFO]", "blue")}: LOG FILE WAS SENT SUCCESSFULLY')
    except Exception as e:
        await kreacher.send_message(f"__Master, something has happened.__\n\n `Error: {e}`")
        logging.error(e)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_log())
