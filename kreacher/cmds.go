package main

import (
	"fmt"

	tele "gopkg.in/telebot.v3"
	tmdw "gopkg.in/telebot.v3/middleware"
	cm "santiirepair.dev/kreacher/commands"
)

func cmds(ck CKreacher, cf KConfig) {
	adminMdw := tmdw.Whitelist([]int64{1027242622}...)

	ck.Bot.Handle(config, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	ck.Bot.Handle(config, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	ck.Bot.Handle(help, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	ck.Bot.Handle(leave, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	ck.Bot.Handle(ping, func(c tele.Context) error {
		sent := cm.Ping(c)

		if sent != nil {
			panic(sent.Error())
		}

		return sent
	})

	ck.Bot.Handle(playBook, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	ck.Bot.Handle(playSong, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	ck.Bot.Handle(playVideo, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	ck.Bot.Handle(streaming, func(c tele.Context) error {
		fmt.Println("Got a hello message")
		sent := c.Send("Hello to you too!")
		if sent != nil {
			panic(sent.Error())
		}
		return sent
	})

	ck.Bot.Handle(shell, func(c tele.Context) error {
		sent := cm.Shell(c)

		if sent != nil {
			panic(sent.Error())
		}

		return sent
	}, adminMdw)

	ck.Bot.Handle(speedtest, func(c tele.Context) error {
		sent := cm.Speedtest(c)

		if sent != nil {
			panic(sent.Error())
		}
		return sent
	}, adminMdw)
}
