package commands

import (
	"context"
	"fmt"
	"log"

	"go.uber.org/zap"
	tele "gopkg.in/telebot.v3"
	"gopkg.in/telebot.v3/middleware"
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
	mantainer, err := core.U.Self(context.Background())
	if err != nil {
		log.Fatalln(err)
	}

	onlyAdmin := middleware.Whitelist([]int64{mantainer.ID}...)

	core.B.Handle(CONFIG, func(c tele.Context) error {
		sent := c.Send("Hello to you too!")
		if sent != nil {
			logger.Error("config command", zap.Error(sent))
		}

		return nil
	})

	core.B.Handle(HELP, func(c tele.Context) error {
		if sent := c.Send(
			"For info on how to use the bot we recommend reading our [wiki](https://github.com/SantiiRepair/kreacher-bot/wiki)",
			tele.ParseMode(tele.ModeMarkdownV2),
			tele.NoPreview,
		); sent != nil {
			logger.Error("help command", zap.Error(sent))
		}

		return nil
	})

	core.B.Handle(LEAVE, func(c tele.Context) error {
		sent := leave(c)
		if sent != nil {
			logger.Error("leave command", zap.Error(sent))
		}

		return nil
	})

	core.B.Handle(ACCIO, func(c tele.Context) error {
		sent := accio(c)
		if sent != nil {
			logger.Error("accio command", zap.Error(sent))
		}

		return nil
	})

	core.B.Handle(PLAY_BOOK, func(c tele.Context) error {
		sent := c.Send("Hello to you too!")
		if sent != nil {
			logger.Error("play book command", zap.Error(sent))
		}

		return nil
	})

	core.B.Handle(PLAY_SONG, func(c tele.Context) error {
		if c.Chat().Type == tele.ChatPrivate {
			return c.Send("*_This command is only for groups or channels_*", tele.ParseMode(tele.ModeMarkdownV2))
		}

		sent := play(c)
		if sent != nil {
			logger.Error("play audio command", zap.Error(sent))
		}

		return nil
	})

	core.B.Handle(PLAY_VIDEO, func(c tele.Context) error {
		if c.Chat().Type == tele.ChatPrivate {
			return c.Send("*_This command is only for groups or channels_*", tele.ParseMode(tele.ModeMarkdownV2))
		}

		sent := vplay(c)
		if sent != nil {
			logger.Error("play video command", zap.Error(sent))
		}

		return nil
	})

	core.B.Handle(STREAMING, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			logger.Error("streaming command", zap.Error(sent))
		}

		return nil
	})

	core.B.Handle(SH, func(c tele.Context) error {
		sent := sh(c)
		if sent != nil {
			logger.Error("sh command", zap.Error(sent))
		}

		return nil
	}, onlyAdmin)

	core.B.Handle(LOGS, func(c tele.Context) error {
		sent := logs(c)
		if sent != nil {
			logger.Error("logs command", zap.Error(sent))
		}

		return nil
	}, onlyAdmin)

	core.B.Handle(SPEEDTEST, func(c tele.Context) error {
		sent := speedtest(c)
		if sent != nil {
			logger.Error("speedtest command", zap.Error(sent))
		}

		return nil
	}, onlyAdmin)
}

var forgottenUsage = `
It seems you forgot something 🤔\!

If you have any questions or problems with the command we recommend reading our [wiki](https://github.com/SantiiRepair/kreacher-bot/wiki/Usage#play)
`

var urlMitasken = `
There seems to be a problem, why?

• URL is invalid
• Youtube Endpoint crashing
• The file is corrupted
`
