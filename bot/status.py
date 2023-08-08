import functools


def is_admin(func):
    @functools.wraps(func)
    async def a_c(message):
        is_admin = False
        if not message.is_private:
            try:
                _s = await message.client.get_permissions(
                    message.chat_id, message.sender_id
                )
                if _s.is_admin:
                    is_admin = True
            except:
                is_admin = False
        if is_admin:
            await func(message, _s)
        else:
            await message.reply("Only Admins can execute this command!")

    return a_c
