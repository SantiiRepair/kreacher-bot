package kreacher

import (
	td "github.com/gotd/td/telegram"
	redis "github.com/redis/go-redis/v9"
	tele "gopkg.in/telebot.v3"
)

type Kreacher struct {
	RedisDB     *redis.Client
	KreacherBot *tele.Bot
	UserBot     *td.Client
}

func NewKreacher(redisDB *redis.Client, kreacherBot *tele.Bot, userBot *td.Client) *Kreacher {
	return &Kreacher{
		RedisDB:     redisDB,
		KreacherBot: kreacherBot,
		UserBot:     userBot,
	}

}
