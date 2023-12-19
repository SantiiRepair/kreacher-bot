import logging
from bot import kreacher


async def user_info(user) -> dict:
    try:
        info = await kreacher.get_users(user.id)
        data = info.__dict__
        if info.username:
            data["mention"] = f"https://t.me/{info.username}"
            return data
        data["mention"] = f"tg://user?id={user.id}"
        return data
    except Exception as e:
        logging.error(e)
