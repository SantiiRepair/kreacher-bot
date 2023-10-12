import logging


def bytes_to_string(byte_count):
    """Converts a byte count to a string (in KB, MB...)"""
    suffix_index = 0
    while byte_count >= 1024:
        byte_count /= 1024
        suffix_index += 1

    return "{:.2f}{}".format(
        byte_count, [" bytes", "KB", "MB", "GB", "TB"][suffix_index]
    )


async def progress(current_bytes, total_bytes, client, chat_id, _message):
    try:
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=_message.id,
            text=f"💾 **__Downloading...__** **{(current_bytes / total_bytes):.2%}**",
        )

    except Exception as err:
        logging.error(err)
