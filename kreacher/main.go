package main

import (
	"database/sql"
	"fmt"
	"time"

	td "github.com/gotd/td/telegram"
	_ "github.com/lib/pq"
	redis "github.com/redis/go-redis/v9"
	tele "gopkg.in/telebot.v3"
)

func main() {
	logger, err := NewLogger("kreacher", "kreacher.log")

	if err != nil {
		panic(err)
	}

	postgresDB, err := sql.Open("postgres", "user=username password=password dbname=database sslmode=disable")

	if err != nil {
		panic(err)
	}

	defer postgresDB.Close()

	redisDB := redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%d", NewConfig().RedisHost, NewConfig().RedisPort),
		Password: NewConfig().RedisPassword,
		DB:       0, // use default DB
		Protocol: 3, // specify 2 for RESP 2 or 3 for RESP 3
	})

	defer redisDB.Close()

	bot, err := tele.NewBot(tele.Settings{
		Token:  NewConfig().BotToken,
		Poller: &tele.LongPoller{Timeout: 10 * time.Second},
	})

	if err != nil {
		panic(err)
	}

	defer bot.Close()

	userBot := td.NewClient(NewConfig().APIID, NewConfig().APIHash, td.Options{})

	kreacher := NewClient(
		logger,
		bot,
		userBot,
		redisDB,
	)

	err = kreacher.Bot.SetCommands([]tele.Command{
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
}