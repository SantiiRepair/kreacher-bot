package main

import (
	"context"
	"fmt"
	"time"

	td "github.com/gotd/td/telegram"
	_ "github.com/lib/pq"
	redis "github.com/redis/go-redis/v9"
	tele "gopkg.in/telebot.v3"
)

func main() {
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
			DB:       0,
			Protocol: 3,
		},
		DB: &DB{
			DriverName: "postgres",
			DriverConn: "user=username password=password dbname=database sslmode=disable",
		},
	}

	kreacher := NewClient(&kparams)

	err := kreacher.Bot.SetCommands([]tele.Command{
		{Text: "config", Description: "Set the bot's configuration"},
		{Text: "help", Description: "How to use this"},
		{Text: "leave", Description: "Leave the voice chat"},
		{Text: "ping", Description: "Check the server's latency"},
		{Text: "play_book", Description: "Play a pdf or epub file as an audio book"},
		{Text: "play_song", Description: "Play audio in the voice chat"},
		{Text: "play_video", Description: "Play video in the voice chat"},
		{Text: "speedtest", Description: "Run server speed test"},
		{Text: "streaming", Description: "Any movie or series"},
	})

	if err != nil {
		panic(err)
	}

	if err := kreacher.UserBot.Run(context.Background(), func(ctx context.Context) error {
		// It is only valid to use client while this function is not returned
		// and ctx is not cancelled.
		user, err := kreacher.UserBot.Self(context.Background())
		if err != nil {
			panic(err)
		}
		// Now you can invoke MTProto RPC requests by calling the API.
		// ...

		// Return to close client connection and free up resources.
		fmt.Println(user.FirstName)
		return nil
	}); err != nil {
		panic(err)
	}

}
