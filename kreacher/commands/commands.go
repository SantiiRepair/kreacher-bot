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
	START      string = "/start"
	CONFIG     string = "/config"
	HELP       string = "/help"
	LEAVE      string = "/leave"
	PING       string = "/ping"
	PLAY_BOOK  string = "/play_book"
	PLAY_SONG  string = "/play_song"
	PLAY_VIDEO string = "/play_video"
	SH         string = "/sh"
	SPEEDTEST  string = "/speedtest"
	STREAMING  string = "/streaming"
)

func Start() {
	rawObj, err := inst.U.ResolveUsername(cfg.BotConfig().Maintainer)
	if err != nil {
		log.Fatalln(err)
	}

	mantainer := rawObj.(*tg.UserObj)

	onlyAdmin := middleware.Whitelist([]int64{mantainer.ID}...)

	inst.B.Handle(CONFIG, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	inst.B.Handle(HELP, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	inst.B.Handle(LEAVE, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	inst.B.Handle(PING, func(c tele.Context) error {
		sent := ping(c)

		if sent != nil {
			panic(sent.Error())
		}

		return sent
	})

	inst.B.Handle(PLAY_BOOK, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	inst.B.Handle(PLAY_SONG, func(c tele.Context) error {
		if c.Chat().Type == tele.ChatPrivate {
			return c.Send("*_This command is only for groups or channels_*", tele.ParseMode(tele.ModeMarkdownV2))
		}

		sent := playSong(c)
		if sent != nil {
			panic(sent.Error())
		}

		return sent
	})

	inst.B.Handle(PLAY_VIDEO, func(c tele.Context) error {
		if c.Chat().Type == tele.ChatPrivate {
			return c.Send("*_This command is only for groups or channels_*", tele.ParseMode(tele.ModeMarkdownV2))
		}

		sent := playVideo(c)
		if sent != nil {
			panic(sent.Error())
		}

		return sent
	})

	inst.B.Handle(STREAMING, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	inst.B.Handle(SH, func(c tele.Context) error {
		sent := sh(c)

		if sent != nil {
			panic(sent.Error())
		}

		return sent
	}, onlyAdmin)

	inst.B.Handle(SPEEDTEST, func(c tele.Context) error {
		sent := speedtest(c)

		if sent != nil {
			logger.Error(sent.Error())
		}

		return sent
	}, onlyAdmin)
}
