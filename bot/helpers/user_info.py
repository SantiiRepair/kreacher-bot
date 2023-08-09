import logging
from bot import kreacher


async def user_info(user) -> dict:
    try:
        data = await kreacher.get_users(user.id)
        join = data.__dict__
        if data.username:
            join.append({"linked": f"https://t.me/{data.username}"})
            return join
        join.append({"linked": f"https://t.me/adduser?id={user.id}"})
        return join
    except Exception as e:
        logging.error(e)
