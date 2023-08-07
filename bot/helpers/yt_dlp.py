import asyncio
import os
import os.path
from yt_dlp import YoutubeDL
from bot import kreacher as bot
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
)

LOGS = {}
SUDO_USERS = {}


async def is_admin(chat_id, user_id):
    req_jo = await bot(GetParticipantRequest(channel=chat_id, user_id=user_id))
    chat_participant = req_jo.participant
    if isinstance(chat_participant, ChannelParticipantCreator) or isinstance(
        chat_participant, ChannelParticipantAdmin
    ):
        return True
    return False


async def bash(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


ydl_opts = {
    "format": "bestaudio[ext=m4a]",
    "geo-bypass": True,
    "noprogress": True,
    "user-agent": "Mozilla/5.0 (Linux; Android 7.0; k960n_mt6580_32_n) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
    "extractor-args": "youtube:player_client=all",
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)


def download_lagu(url: str) -> str:
    info = ydl.extract_info(url, download=False)
    ydl.download([url])
    return os.path.join("downloads", f"{info['id']}.{info['ext']}")
