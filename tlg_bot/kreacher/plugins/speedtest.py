from telethon import events
from kreacher import *
import asyncio
import speedtest


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        test.download()
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception:
        return
    return result


msg_running = """<i>Kreacher is here to serve you.

Running Speedtest...</i> \U0001F4F6"""


@kreacher.on(events.NewMessage(pattern="^/speedtest"))
async def speedtest_function(message):
    m = await message.reply(msg_running, parse_mode="HTML")
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""**Speedtest Results**

**Client:**
**__ISP:__** {result['client']['isp']}
**__Country:__** {result['client']['country']}
  
**Server:**
**__Name:__** {result['server']['name']}
**__Country:__** {result['server']['country']}, {result['server']['cc']}
**__Sponsor:__** {result['server']['sponsor']}
**__Latency:__** {result['server']['latency']} 
**__Ping:__** {result['ping']}"""
    await kreacher.send_file(message.chat.id, result["share"], caption=output)
    await m.delete()
