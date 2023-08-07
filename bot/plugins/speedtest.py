import asyncio
from bot import kreacher
from telethon import events
from speedtest import Speedtest


def testspeed(m):
    try:
        test = Speedtest()
        test.get_best_server()
        test.download()
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception:
        return
    return result


@kreacher.on(events.NewMessage(pattern="^[!?/]speedtest"))
async def speed_test(event):
    message = await event.reply(
        """__Kreacher is here to serve you.

Running Speedtest...__ \U0001F4F6"""
    )
    await event.delete()
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, message)
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
    await kreacher.send_file(event.chat.id, result["share"], caption=output)
    return await message.delete()
