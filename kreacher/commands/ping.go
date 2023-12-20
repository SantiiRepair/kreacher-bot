package commands

import tele "gopkg.in/telebot.v3"

func Ping(c tele.Context) error {

	err := c.Send("<b><i>PONG!!</i></b>", &tele.ReplyMarkup{InlineKeyboard: [][]tele.InlineButton{
		{
			tele.InlineButton{
				Text: "🏓",
				Data: "ping_cbk",
			},
		},
	}},
		tele.ParseMode(tele.ModeHTML),
	)

	return err
}
