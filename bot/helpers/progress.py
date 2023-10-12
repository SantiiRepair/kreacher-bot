import logging


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
