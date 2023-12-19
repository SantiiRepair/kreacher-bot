package main

import (
	"log"

	td "github.com/gotd/td/telegram"
	redis "github.com/redis/go-redis/v9"
	tele "gopkg.in/telebot.v3"
)

type Kreacher struct {
	Logger  *log.Logger
	Bot     *tele.Bot
	UserBot *td.Client
	RedisDB *redis.Client
}

func NewClient(
	logger *log.Logger,
	kreacherBot *tele.Bot,
	userBot *td.Client,
	redisDB *redis.Client,
) *Kreacher {

	return &Kreacher{
		Logger:  logger,
		Bot:     kreacherBot,
		UserBot: userBot,
		RedisDB: redisDB,
	}
}
