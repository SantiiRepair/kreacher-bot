from telethon import events
from tlg_bot import kreacher
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


@kreacher.on(events.NewMessage(pattern="[!?/]speedtest"))
async def speedtest_function(message):
    m = await message.reply(
        """__Kreacher is here to serve you.

Running Speedtest...__ \U0001F4F6"""
    )
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""**Speedtest Results**

**Client**:
**__ISP__**: {result['client']['isp']}
**__Country__**: {result['client']['country']}</i>

**Server**:
**__Name__**: {result['server']['name']}
**__Country:__** {result['server']['country']}, {result['server']['cc']}
**__Sponsor:__** {result['server']['sponsor']}
**__Latency__**: {result['server']['latency']} 
**__Ping__**: {result['ping']}</i></b>"""
    await kreacher.send_file(message.chat.id, result["share"], caption=output)
    await m.delete()
