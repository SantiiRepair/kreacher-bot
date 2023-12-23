<div align="center">

<img src="https://static.scarf.sh/a.png?x-pxid=cf317fe7-2188-4721-bc01-124bb5d5dbb2" />

## <img alt="Kreacher Logo" src="https://github.com/SantiiRepair/kreacher-bot/blob/main/.github/images/kreacher-srd-circle.png?raw=true" width="25%"/>

### Kreacher | Streamer 🎬

##### [@KreacherStreamerBot](https://t.me/KreacherStreamerBot)

##### Kreacher can stream books, songs, videos, movies and series in any group or channel via voice chat 🔮
______________________________________________________________________
[![License](https://img.shields.io/badge/License-GPL--3.0-magenta.svg)](https://www.gnu.org/licenses/gpl-3.0.txt)
[![Kreacher Streamer Channel](https://img.shields.io/endpoint?label=Channel&style=flat-square&url=https://mogyo.ro/quart-apis/tgmembercount?chat_id=KreacherStreamerChannel)](https://t.me/KreacherStreamerChannel)
[![Kreacher Streamer CI](https://img.shields.io/endpoint?label=CI&style=flat-square&url=https%3A%2F%2Fmogyo.ro%2Fquart-apis%2Ftgmembercount%3Fchat_id%3DKreacherStreamerCI)](https://t.me/KreacherStreamerCI)

______________________________________________________________________

</div>

## Setting Up
First of all you must create a `.env` file that contains access keys, database configurations, etc... you can do it by copying and pasting the `.env.example` file and renaming it to just `.env` then fill out the fields, you can get the `API_ID` and `API_HASH` [here](https://my.telegram.org/) the bot uses [Telegram's MTProto API](https://core.telegram.org/mtproto) to download large files faster since the bot api is [limited](https://core.telegram.org/bots/faq#how-do-i-download-files) to only 20MB and the download is slower.

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
