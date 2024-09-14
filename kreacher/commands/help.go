package commands

import tele "gopkg.in/telebot.v3"

func help(c tele.Context) error {

	return c.Send(
		"For info on how to use the bot we recommend reading our [wiki](https://github.com/SantiiRepair/kreacher-bot/wiki)",
		tele.ParseMode(tele.ModeMarkdownV2),
		tele.NoPreview,
	)
}
