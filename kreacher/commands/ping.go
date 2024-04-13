package commands

import tele "gopkg.in/telebot.v3"

func ping(c tele.Context) error {

	err := c.Send(pong, &tele.ReplyMarkup{InlineKeyboard: [][]tele.InlineButton{
		{
			{
				Text:   "🏓",
				Unique: "ping",
				Data:   "",
			},
		},
	}},
		tele.ParseMode(tele.ModeHTML),
	)

	return err
}

var pong = "<b><i>PONG!!</i></b>"
