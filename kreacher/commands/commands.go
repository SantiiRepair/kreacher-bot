package commands

import "gopkg.in/telebot.v3"

type Commands interface {
	Actives()
	Ping(c telebot.Context) error
}