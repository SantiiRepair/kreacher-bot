package commands

import (
	"context"
	"log"

	"gopkg.in/telebot.v3/middleware"
	"santiirepair.dev/kreacher/core"
)

const (
	START      string = "/start"
	CONFIG     string = "/config"
	HELP       string = "/help"
	LEAVE      string = "/leave"
	ACCIO      string = "/accio"
	PLAY_BOOK  string = "/bplay"
	PLAY_AUDIO string = "/play"
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

	core.B.Handle(CONFIG, config)

	core.B.Handle(HELP, help)
	core.B.Handle(LEAVE, leave)
	core.B.Handle(ACCIO, accio)

	core.B.Handle(PLAY_BOOK, bplay)
	core.B.Handle(PLAY_AUDIO, play)
	core.B.Handle(PLAY_VIDEO, vplay)
	core.B.Handle(STREAMING, streaming)

	core.B.Handle(SH, sh, onlyAdmin)
	core.B.Handle(LOGS, logs, onlyAdmin)
	core.B.Handle(SPEEDTEST, speedtest, onlyAdmin)
}

var forgottenUsage = `
It seems you forgot something 🤔\!

If you have any questions or problems with the command we recommend reading our [wiki](https://github.com/SantiiRepair/kreacher-bot/wiki/Usage#play)
`

var urlMistaken = `
There seems to be a problem, why?

• URL is invalid
• Youtube Endpoint crashing
• The file is corrupted
`
