package main

import (
	"fmt"

	tele "gopkg.in/telebot.v3"
	tmdw "gopkg.in/telebot.v3/middleware"
	cm "santiirepair.dev/kreacher/commands"
)

func cmds() {
	adminMdw := tmdw.Whitelist([]int64{1027242622}...)

	bot.Handle(config, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

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
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	bot.Handle(playVideo, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
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
	}, adminMdw)

	bot.Handle(speedtest, func(c tele.Context) error {
		sent := cm.Speedtest(c)

		if sent != nil {
			fmt.Println(sent.Error())
			Error(sent.Error())
		}

		return sent
	}, adminMdw)
}
