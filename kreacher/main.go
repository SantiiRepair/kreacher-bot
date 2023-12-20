package main

import (
	"fmt"
	"time"

	td "github.com/gotd/td/telegram"
	_ "github.com/lib/pq"
	redis "github.com/redis/go-redis/v9"
	"gopkg.in/kreacher-bot.v1/kreacher/commands"
	tele "gopkg.in/telebot.v3"
)

func main() {
	var cm commands.Commands

	kparams := KParams{
		Logger: &Logger{
			Name: "kreacher",
			Path: "kreacher.log",
		},
		Bot: &tele.Settings{
			Token:  BotConfig().BotToken,
			Poller: &tele.LongPoller{Timeout: 10 * time.Second},
		},
		UserBot: &MTProto{
			APIID:   BotConfig().APIID,
			APIHash: BotConfig().APIHash,
			Options: &td.Options{},
		},
		RedisDB: &redis.Options{
			Addr:     fmt.Sprintf("%s:%d", BotConfig().RedisHost, BotConfig().RedisPort),
			Password: BotConfig().RedisPassword,
			DB:       0, // use default DB
			Protocol: 3, // specify 2 for RESP 2 or 3 for RESP 3
		},
		DB: &DB{
			DriverName: "postgres",
			DriverConn: "user=username password=password dbname=database sslmode=disable",
		},
	}

	k, err := Kreacher(&kparams)

	if err != nil {
		panic(err)
	}

	if err := k.Bot.SetCommands([]tele.Command{
		{Text: "config", Description: "Set the bot's configuration"},
		{Text: "help", Description: "How to use this"},
		{Text: "leave", Description: "Leave the voice chat"},
		{Text: "ping", Description: "Check the server's latency"},
		{Text: "play_book", Description: "Play a pdf or epub file as an audio book"},
		{Text: "play_song", Description: "Play audio in the voice chat"},
		{Text: "play_video", Description: "Play video in the voice chat"},
		{Text: "speedtest", Description: "Run server speed test"},
		{Text: "streaming", Description: "Any movie or series"},
	}); err != nil {
		panic(err)
	}

	// Commands ############################################################### //

	k.Bot.Handle(Config, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	k.Bot.Handle(Help, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	k.Bot.Handle(Leave, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	k.Bot.Handle(Ping, func(c tele.Context) error {
		sent := cm.Ping(c)

		if sent != nil {
			panic(sent.Error())
		}

		return sent
	})

	k.Bot.Handle(PlayBook, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	k.Bot.Handle(PlaySong, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	k.Bot.Handle(PlayVideo, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	k.Bot.Handle(Speedtest, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	k.Bot.Handle(Streaming, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	k.Bot.Start()
}
