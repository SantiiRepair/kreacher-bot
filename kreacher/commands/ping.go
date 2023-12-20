package commands

import tele "gopkg.in/telebot.v3"

func Ping(c tele.Context, message string) (error) {
	err := c.Send(
		"**__PONG__**",
	)

    if err != nil {
        return err
    }

    return err
}
