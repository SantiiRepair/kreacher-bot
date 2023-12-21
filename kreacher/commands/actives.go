package commands

import tele "gopkg.in/telebot.v3"

func Actives(c tele.Context) error {
	err := c.Send("<b><i>Getting active Voice Chats... \n\nPlease hold, master</i></b>", tele.ParseMode(tele.ModeHTML))

	if err != nil {
		return err
	}

	err = c.Send("<b><i>No active Voice Chats</i></b>", tele.ParseMode(tele.ModeHTML))

	return err
}
