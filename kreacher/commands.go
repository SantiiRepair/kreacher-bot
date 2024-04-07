package main

import (
	"fmt"
	"log"

	tg "github.com/amarnathcjd/gogram/telegram"
	tele "gopkg.in/telebot.v3"
	middleware "gopkg.in/telebot.v3/middleware"
	cm "santiirepair.dev/kreacher/commands"
)

func commands() {
	rawObj, err := ubot.ResolveUsername(BotConfig().Maintainer)
	if err != nil {
		log.Fatalln(err)
	}

	mantainer := rawObj.(*tg.UserObj)

	onlyAdmin := middleware.Whitelist([]int64{mantainer.ID}...)

	bot.Handle(config, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	bot.Handle(help, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	bot.Handle(leave, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	bot.Handle(ping, func(c tele.Context) error {
		sent := cm.Ping(c)

		if sent != nil {
			panic(sent.Error())
		}

		return sent
	})

	bot.Handle(playBook, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	bot.Handle(playSong, func(c tele.Context) error {
		if c.Chat().Type == tele.ChatPrivate {
			return c.Send("*_This command is only for groups or channels_*", tele.ParseMode(tele.ModeMarkdownV2))
		}

		sent := cm.PlaySong(c, ubot, ntgcalls)
		if sent != nil {
			panic(sent.Error())
		}

		return sent
	})

	bot.Handle(playVideo, func(c tele.Context) error {
		if c.Chat().Type == tele.ChatPrivate {
			return c.Send("*_This command is only for groups or channels_*", tele.ParseMode(tele.ModeMarkdownV2))
		}

		sent := cm.PlayVideo(c, ubot, ntgcalls)
		if sent != nil {
			panic(sent.Error())
		}

		return sent
	})

	bot.Handle(streaming, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	bot.Handle(shell, func(c tele.Context) error {
		sent := cm.Shell(c)

		if sent != nil {
			panic(sent.Error())
		}

		return sent
	}, onlyAdmin)

	bot.Handle(speedtest, func(c tele.Context) error {
		sent := cm.Speedtest(c)

		if sent != nil {
			Error(sent.Error())
		}

		return sent
	}, onlyAdmin)
}
