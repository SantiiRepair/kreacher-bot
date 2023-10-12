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


async def progress(current_bytes, total_bytes, client, chat_id, message_id):
    try:
        percentage = round(((current_bytes / total_bytes) * 100), 2)
        text = f"💾 **__Downloading...__** **{percentage}%**"
        if percentage >= 25 and percentage <= 35:
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
            )
        if percentage >= 50 and percentage <= 60:
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
            )
        if percentage >= 90:
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
            )
    except Exception as err:
        logging.error(err)
