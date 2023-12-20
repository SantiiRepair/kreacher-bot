package main

import (
	"database/sql"
	"fmt"

	td "github.com/gotd/td/telegram"
	_ "github.com/lib/pq"
	redis "github.com/redis/go-redis/v9"
	tele "gopkg.in/telebot.v3"
)

func NewClient(params *KParams) *Kreacher {
	logger, err := NewLogger(params.Logger.Name, params.Logger.Path)

	if err != nil {
		panic(err)
	}

	bot, err := tele.NewBot(tele.Settings{
		Token:  params.Bot.Token,
		Poller: params.Bot.Poller,
	})

	if err != nil {
		panic(err)
	}

	defer bot.Close()

	userBot := td.NewClient(params.UserBot.APIID, params.UserBot.APIHash, *params.UserBot.Options)
	redisDB := redis.NewClient(&redis.Options{
		Addr:     params.RedisDB.Addr,
		Password: params.RedisDB.Password,
		DB:       params.RedisDB.DB,       // use default DB
		Protocol: params.RedisDB.Protocol, // specify 2 for RESP 2 or 3 for RESP 3
	})

	defer redisDB.Close()

	postgresDB, err := sql.Open("postgres", "user=username password=password dbname=database sslmode=disable")

	if err != nil {
		panic(err)
	}

	defer postgresDB.Close()

	return &Kreacher{
		Logger:  logger,
		Bot:     bot,
		UserBot: userBot,
		RedisDB: redisDB,
	}
}
