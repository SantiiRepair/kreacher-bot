import os
import logging
from yt_dlp import YoutubeDL
from bot.helpers.bash import bash
from youtubesearchpython import VideosSearch

LOGS = {}
SUDO_USERS = {}


ydl = YoutubeDL(
    {
        "format": "bestaudio[ext=m4a]",
        "geo-bypass": True,
        "noprogress": True,
        "user-agent": "Mozilla/5.0 (Linux; Android 7.0; k960n_mt6580_32_n) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
        "extractor-args": "youtube:player_client=all",
        "nocheckcertificate": True,
        "outtmpl": "downloads/%(id)s.%(ext)s",
    }
)


def download_lagu(url: str) -> str:
    info = ydl.extract_info(url, download=False)
    ydl.download([url])
    return os.path.join("downloads", f"{info['id']}.{info['ext']}")


async def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        name = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        videoid = data["id"]
        return [name, url, duration, thumbnail, videoid]
    except Exception as e:
        logging.error(e)
        return 0


async def ytdl(fmt: str, link: str):
    try:
        stdout, stderr = await bash(f'yt-dlp -g -f "{fmt}" {link}')
        if stdout:
            return 1, stdout.split("\n")[0]
        return 0, stderr
    except Exception as e:
        logging.error(e)
        return 0