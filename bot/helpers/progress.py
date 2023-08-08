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


def progress_callback(downloaded_bytes, total_bytes):
    logging.info(
        "{} {} out of {} ({:.2%})".format(
            progress_type,
            bytes_to_string(downloaded_bytes),
            bytes_to_string(total_bytes),
            downloaded_bytes / total_bytes,
        )
    )
