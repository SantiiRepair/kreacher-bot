import logging
from random import randint


def bytes_to_string(byte_count):
    """Converts a byte count to a string (in KB, MB...)"""
    suffix_index = 0
    while byte_count >= 1024:
        byte_count /= 1024
        suffix_index += 1

    return "{:.2f}{}".format(
        byte_count, [" bytes", "KB", "MB", "GB", "TB"][suffix_index]
    )


async def progress(current_bytes, total_bytes, client, chat_id, message_id):
    try:
        percentage = current_bytes / total_bytes
        print(percentage)
        text = f"💾 **__Downloading...__** **{percentage:.2%}**"
        if percentage >= randint(20, 30):
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
            )
        if percentage >= randint(50, 60):
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
            )
        if percentage >= randint(70, 80):
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
            )
        if percentage >= randint(90, 100):
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
            )
    except Exception as err:
        logging.error(err)
