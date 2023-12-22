<div align="center">
<img src="https://static.scarf.sh/a.png?x-pxid=cf317fe7-2188-4721-bc01-124bb5d5dbb2" />

## <img src="https://github.com/SantiiRepair/kreacher-bot/blob/main/.github/images/kreacher-srd.png?raw=true" height="156" style="border-radius: 20px;"/>


**Streamer of videos and songs in any Telegram Voice Chat.**

______________________________________________________________________

[![Kreacher Streamer Bot](https://img.shields.io/badge/bot-grey?logo=telegram&logoColor=%20%230088cc&label=telegram&labelColor=blue&color=grey)](https://t.me/KreacherStreamerBot)

</div>

______________________________________________________________________

## Setting Up
First of all you must create a `.env` file that contains access keys, database configurations, etc... you can do it by copying and pasting the `.env.example` file and renaming it to just `.env` then fill out the fields, you can get the API_ID and API_HASH [here](https://my.telegram.org/) the bot uses [Telegram's MTProto API](https://core.telegram.org/mtproto) to download large files faster since the bot api is [limited](https://core.telegram.org/bots/faq#how-do-i-download-files) to only 20MB and the download is slower.

If you will be running the bot locally you can run the following command to install some necessary things:

```sh
$ bash setenv.sh --local
```

This will install postgres, redis, google chrome and other things if they are not installed.

## Running
If everything is configured you just need to run the following command to run the bot:

```sh
$ make start
```

If you ran it in docker you can do it with:

```sh
$ make docker
```

## Disclaimer
This project is a work in progress.