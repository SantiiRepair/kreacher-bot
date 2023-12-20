package commands

import tele "gopkg.in/telebot.v3"

func Actives(c tele.Context, message string) (error) {
	err := c.Send(
		"**__Getting active Voice Chats... \n\nPlease hold, master__**",
	)
    
    if err != nil {
        return err
    }

	err = c.Send("**__No active Voice Chats__**")
    return err
}
