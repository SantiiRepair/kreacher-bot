import asyncio
import logging

# pylint: disable=import-self
from speedtest import Speedtest
from pyrogram.types import Message
from pyrogram import filters, Client

from bot import kreacher


def testspeed():
    try:
        test = Speedtest()
        test.get_best_server()
        test.download()
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception as err:
        logging.error(err)
        raise err
    return result


@kreacher.on_message(filters.regex(pattern="^[!?/]speedtest"))
async def _(client: Client, message: Message):
    chat = message.chat
    try:
        msg = await message.reply(
            """**__Kreacher is here to serve you.

Running Speedtest...__** 📶"""
        )

        ay = asyncio.get_event_loop()
        result = await ay.run_in_executor(None, testspeed)

        output = f"""**Speedtest Results**

**Client**:
**__ISP__**: {result['client']['isp']}
**__Country__**: {result['client']['country']}

**Server**:
**__Name__**: {result['server']['name']}
**__Country:__** {result['server']['country']}, {result['server']['cc']}
**__Sponsor:__** {result['server']['sponsor']}
**__Latency__**: {result['server']['latency']} 
**__Ping__**: {result['ping']}"""
        await kreacher.send_photo(chat.id, photo=result["share"], caption=output)
        return await msg.delete()
    except Exception as err:
        return await msg.edit(
            f"__Oops master, something wrong has happened.__ \n\n`Error: {err}`",
        )
