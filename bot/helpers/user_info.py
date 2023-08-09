import logging
from bot import kreacher


async def user_info(user) -> dict:
    try:
        info = await kreacher.get_users(user.id)
        data = info.__dict__
        if info.username:
            data["linked"] = f"https://t.me/{info.username}"
            return data
        data["linked"] = f"https://t.me/adduser?id={user.id}"
        return data
    except Exception as e:
        logging.error(e)
