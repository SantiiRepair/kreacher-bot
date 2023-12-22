package main

import (
	"database/sql"
	"fmt"
	"time"

	tele "gopkg.in/telebot.v3"

	td "github.com/gotd/td/telegram"
	_ "github.com/lib/pq"
	redis "github.com/redis/go-redis/v9"
)

func init() {
	ibot, err := tele.NewBot(tele.Settings{
		Token:  botConfig().BotToken,
		Poller: &tele.LongPoller{Timeout: 10 * time.Second},
		OnError: func(err error, ctx tele.Context) {
			Error(err.Error())
		},
	})

	if err != nil {
		panic(err)
	}

	defer ibot.Close()

	iubot := td.NewClient(botConfig().APIID, botConfig().APIHash, td.Options{})

	irdc := redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%d", botConfig().RedisHost, botConfig().RedisPort),
		Password: botConfig().RedisPassword,
		DB:       0, // use default DB
		Protocol: 3, // specify 2 for RESP 2 or 3 for RESP 3
	})

	defer irdc.Close()

	idb, err := sql.Open("postgres", "user=username password=password dbname=database sslmode=disable")

	if err != nil {
		panic(err)
	}

	defer idb.Close()

	// Set client instances to late vars in vars.go file.

	bot = ibot
	ubot = iubot
	rdc = irdc
	db = idb
}

func main() {

	if err := bot.SetCommands([]tele.Command{
		{Text: "config", Description: "Set the bot's configuration"},
		{Text: "help", Description: "How to use this"},
		{Text: "leave", Description: "Leave the voice chat"},
		{Text: "ping", Description: "Check the server's latency"},
		{Text: "play_book", Description: "Play a pdf or epub file as an audio book"},
		{Text: "play_song", Description: "Play audio in the voice chat"},
		{Text: "play_video", Description: "Play video in the voice chat"},
		{Text: "streaming", Description: "Any movie or series"},
	}); err != nil {
		panic(err)
	}

	cmds()

	cy.Printf("\nBot @%s started, receiving updates...", bot.Me.Username)

	bot.Start()

}
