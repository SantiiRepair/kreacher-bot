import logging
from bot import kreacher


async def linked(user) -> dict:
    try:
        data = await kreacher.get_users(user.id)
        if data.username:
            return {
                "first_name": data.first_name,
                "linked": f"https://t.me/{data.username}",
            }
        else:
            return {
                "first_name": data.first_name,
                "linked": f"https://t.me/adduser?id={user.id}",
            }
    except Exception as e:
        logging.error(e)
