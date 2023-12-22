## Kreacher
Streamer of videos and songs in an Telegram Voice Chat.

### Setting Up
First of all you must create a `.env` file that contains access keys, database configurations, etc... you can do it by copying and pasting the `.env.example` file and renaming it to just `.env` then fill out the fields, you can get the API_ID and API_HASH (here)[https://my.telegram.org/] the bot uses Telegram's MTProto API to download large files faster since the bot api is limited to only 20MB and The download is slower.

If you will be running the bot locally you can run the following command to install some necessary things:

```sh
$ bash setenv.sh --local
```

This will install postgres, redis, google chrome and other things if they are not installed.

### Running
If everything is configured you just need to run the following command to run the bot:

```sh
$ make start
```

If you ran it in docker you can do it with:

```sh
$ make docker
```

### Disclaimer
This project is a work in progress.