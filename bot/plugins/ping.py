from time import time
from bot import kreacher
from pyrogram import filters
from datetime import datetime


START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (
    ("Week", 60 * 60 * 24 * 7),
    ("Day", 60 * 60 * 24),
    ("Hour", 60 * 60),
    ("Min", 60),
    ("Sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(
                "{} {}{}".format(amount, unit, "" if amount == 1 else "s")
            )
    return ", ".join(parts)


@kreacher.on_message(filters.regex(pattern="^[!?/]ping"))
async def _(client, message):
    start = time()
    current_time = datetime.utcnow()
    delta_ping = time() - start
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply(
        f"__Haha my master, PONG\n\n {delta_ping * 1000:.3f}ms.\n\n Active since {uptime}.__",
    )
