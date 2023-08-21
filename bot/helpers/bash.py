import asyncio
import logging


async def bash(cmd):
    try:
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        err = stderr.decode().strip()
        out = stdout.decode().strip()
        return out, err
    except Exception as e:
        logging.error(e)
        raise e
