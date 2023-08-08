from pyrogram import types
from pyrogram.utils import get_peer_type


def mention(user):
    full_name = get_peer_type(user)
    if not isinstance(user, types.User):
        return full_name
    return f"[{full_name}](tg://user?id={user.id})"
