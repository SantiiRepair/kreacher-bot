package commands

import (
	"fmt"
	"log"

	tg "github.com/amarnathcjd/gogram/telegram"
	tele "gopkg.in/telebot.v3"
	middleware "gopkg.in/telebot.v3/middleware"
	cfg "santiirepair.dev/kreacher/config"
	inst "santiirepair.dev/kreacher/instances"
	"santiirepair.dev/kreacher/logger"
)

const (
	config    string = "/config"
	help      string = "/help"
	leave     string = "/leave"
	ping      string = "/ping"
	playBook  string = "/play_book"
	playSong  string = "/play_song"
	playVideo string = "/play_video"
	shell     string = "/sh"
	speedtest string = "/speedtest"
	streaming string = "/streaming"
)

func init() {
	rawObj, err := inst.U.ResolveUsername(cfg.BotConfig().Maintainer)
	if err != nil {
		log.Fatalln(err)
	}

	mantainer := rawObj.(*tg.UserObj)

	onlyAdmin := middleware.Whitelist([]int64{mantainer.ID}...)

	inst.B.Handle(config, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	inst.B.Handle(help, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	inst.B.Handle(leave, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	inst.B.Handle(ping, func(c tele.Context) error {
		sent := Ping(c)

		if sent != nil {
			panic(sent.Error())
		}

		return sent
	})

	inst.B.Handle(playBook, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	inst.B.Handle(playSong, func(c tele.Context) error {
		if c.Chat().Type == tele.ChatPrivate {
			return c.Send("*_This command is only for groups or channels_*", tele.ParseMode(tele.ModeMarkdownV2))
		}

		sent := PlaySong(c)
		if sent != nil {
			panic(sent.Error())
		}

		return sent
	})

	inst.B.Handle(playVideo, func(c tele.Context) error {
		if c.Chat().Type == tele.ChatPrivate {
			return c.Send("*_This command is only for groups or channels_*", tele.ParseMode(tele.ModeMarkdownV2))
		}

		sent := PlayVideo(c)
		if sent != nil {
			panic(sent.Error())
		}

		return sent
	})

	inst.B.Handle(streaming, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	inst.B.Handle(shell, func(c tele.Context) error {
		sent := Shell(c)

		if sent != nil {
			panic(sent.Error())
		}

		return sent
	}, onlyAdmin)

	inst.B.Handle(speedtest, func(c tele.Context) error {
		sent := Speedtest(c)

		if sent != nil {
			logger.Error(sent.Error())
		}

		return sent
	}, onlyAdmin)
}
