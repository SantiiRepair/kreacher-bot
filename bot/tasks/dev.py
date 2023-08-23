import os
import asyncio
import logging
from bot import kreacher
from bot.config import config
from termcolor import colored


async def send_log():
    c = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(c, "../logs/logs.txt")
    try:
        user = await kreacher.get_users(config.MANTAINER)
        await kreacher.send_document(user.id, document=file)
        print(f'{colored("[INFO]", "blue")}: LOG FILE WAS SENT SUCCESSFULLY')
        with open(file, "w") as f:
            f.truncate(0)
            f.close()
        await kreacher.send_message(
            user.id,
            "__Master, Master, the log file was flushed successfully.__",
        )
        print(
            f'{colored("[INFO]", "blue")}: LOG FILE WAS FLUSHED SUCCESSFULLY'
        )

    except Exception as e:
        await kreacher.send_message(
            user.id, f"__Master, something has happened.__\n\n `Error: {e}`"
        )
        logging.error(e)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_log())
