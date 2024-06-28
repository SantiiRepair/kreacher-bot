package commands

import (
	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/logger"
)

func logs(c tele.Context) error {
	file := &tele.Document{File: tele.FromDisk(logger.LogsPath)}

	return c.Send(file)
}
