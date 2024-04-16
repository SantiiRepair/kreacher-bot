package commands

import tele "gopkg.in/telebot.v3"

func accio(c tele.Context) error {

	err := c.Send(pong, &tele.ReplyMarkup{InlineKeyboard: [][]tele.InlineButton{
		{
			{
				Text:   "🔮",
				Unique: "accio",
				Data:   "",
			},
		},
	}},
		tele.ParseMode(tele.ModeHTML),
	)

	return err
}

var pong = "<b><i>Master!!</i></b>"
