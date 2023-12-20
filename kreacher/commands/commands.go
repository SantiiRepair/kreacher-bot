package commands

import "gopkg.in/telebot.v3"

type Commands interface {
	Actives(telebot.Context) error
	Ping(telebot.Context) error
}