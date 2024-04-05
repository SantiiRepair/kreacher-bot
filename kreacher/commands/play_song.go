package commands

// const re = "^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"

import tele "gopkg.in/telebot.v3"

func PlaySong(c tele.Context) error {

	err := c.Send("", &tele.ReplyMarkup{InlineKeyboard: [][]tele.InlineButton{
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

//var pong = "<b><i>PONG!!</i></b>"
