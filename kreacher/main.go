package kreacher

import (
	"fmt"
	"time"

	td "github.com/gotd/td/telegram"
	redis "github.com/redis/go-redis/v9"
	tele "gopkg.in/telebot.v3"
)

func main() {
	redisDB := redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%d", NewConfig().RedisHost, NewConfig().RedisPort),
		Password: NewConfig().RedisPassword,
		DB:       0, // use default DB
		Protocol: 3, // specify 2 for RESP 2 or 3 for RESP 3
	})

	kreacherBot, _ := tele.NewBot(tele.Settings{
		Token:  NewConfig().BotToken,
		Poller: &tele.LongPoller{Timeout: 10 * time.Second},
	})

	userBot := td.NewClient(NewConfig().APIID, NewConfig().APIHash, td.Options{})

	kreacher := NewKreacher(redisDB, kreacherBot, userBot)

	err := kreacher.KreacherBot.SetCommands([]tele.Command{
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
