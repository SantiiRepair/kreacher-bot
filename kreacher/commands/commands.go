package commands

import (
	"fmt"
	"log"

	tg "github.com/amarnathcjd/gogram/telegram"
	tele "gopkg.in/telebot.v3"
	"gopkg.in/telebot.v3/middleware"
	cfg "santiirepair.dev/kreacher/config"
	"santiirepair.dev/kreacher/core"
	"santiirepair.dev/kreacher/logger"
)

const (
	START      string = "/start"
	CONFIG     string = "/config"
	HELP       string = "/help"
	LEAVE      string = "/leave"
	ACCIO      string = "/accio"
	PLAY_BOOK  string = "/bplay"
	PLAY_SONG  string = "/play"
	PLAY_VIDEO string = "/vplay"
	SH         string = "/sh"
	LOGS       string = "/logs"
	SPEEDTEST  string = "/speedtest"
	STREAMING  string = "/streaming"
)

func Start() {
	rawObj, err := core.U.ResolveUsername(cfg.BotConfig().Maintainer)
	if err != nil {
		log.Fatalln(err)
	}

	mantainer := rawObj.(*tg.UserObj)

	onlyAdmin := middleware.Whitelist([]int64{mantainer.ID}...)

	core.B.Handle(CONFIG, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			logger.Error(sent)
		}
		return sent
	})

	core.B.Handle(HELP, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			logger.Error(sent)
		}
		return sent
	})

	core.B.Handle(LEAVE, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			logger.Error(sent)
		}
		return sent
	})

	core.B.Handle(ACCIO, func(c tele.Context) error {
		sent := accio(c)

		if sent != nil {
			logger.Error(sent)
		}

		return sent
	})

	core.B.Handle(PLAY_BOOK, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			logger.Error(sent)
		}
		return sent
	})

	core.B.Handle(PLAY_SONG, func(c tele.Context) error {
		if c.Chat().Type == tele.ChatPrivate {
			return c.Send("*_This command is only for groups or channels_*", tele.ParseMode(tele.ModeMarkdownV2))
		}

		sent := play(c)
		if sent != nil {
			logger.Error(sent)
		}

		return sent
	})

	core.B.Handle(PLAY_VIDEO, func(c tele.Context) error {
		if c.Chat().Type == tele.ChatPrivate {
			return c.Send("*_This command is only for groups or channels_*", tele.ParseMode(tele.ModeMarkdownV2))
		}

		sent := vplay(c)
		if sent != nil {
			logger.Error(sent)
		}

		return sent
	})

	core.B.Handle(STREAMING, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			logger.Error(sent)
		}
		return sent
	})

	core.B.Handle(SH, func(c tele.Context) error {
		sent := sh(c)

		if sent != nil {
			logger.Error(sent)
		}

		return sent
	}, onlyAdmin)

	core.B.Handle(LOGS, func(c tele.Context) error {
		sent := logs(c)

		if sent != nil {
			logger.Error(sent)
		}

		return sent
	}, onlyAdmin)

	core.B.Handle(SPEEDTEST, func(c tele.Context) error {
		sent := speedtest(c)

		if sent != nil {
			logger.Error(sent)
		}

		return sent
	}, onlyAdmin)
}
