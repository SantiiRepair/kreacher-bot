package main

import (
	"database/sql"

	td "github.com/gotd/td/telegram"
	_ "github.com/lib/pq"
	redis "github.com/redis/go-redis/v9"
	tele "gopkg.in/telebot.v3"
)

func Kreacher(params *KParams) (*CKreacher, error) {
	logger, err := NewLogger(params.Logger.Name, params.Logger.Path)

	if err != nil {
		return nil, err
	}

	bot, err := tele.NewBot(tele.Settings{
		Token:  params.Bot.Token,
		Poller: params.Bot.Poller,
	})

	if err != nil {
		return nil, err
	}

	defer bot.Close()

	userBot := td.NewClient(params.UserBot.APIID, params.UserBot.APIHash, *params.UserBot.Options)

	redisDB := redis.NewClient(&redis.Options{
		Addr:     params.RedisDB.Addr,
		Password: params.RedisDB.Password,
		DB:       params.RedisDB.DB,
		Protocol: params.RedisDB.Protocol,
	})

	defer redisDB.Close()

	db, err := sql.Open(params.DB.DriverName, params.DB.DriverConn) // db sql

	if err != nil {
		return nil, err
	}

	defer db.Close()

	return &CKreacher{
		Logger:  logger,
		Bot:     bot,
		UserBot: userBot,
		RedisDB: redisDB,
		DB:      db,
	}, nil
}
