package commands

import tele "gopkg.in/telebot.v3"

func Ping(c tele.Context) (error) {
	err := c.Send("**__PONG__**")

    return err
}
