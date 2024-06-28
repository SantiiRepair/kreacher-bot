package commands

import (
	"path"

	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/logger"
)

func logs(c tele.Context) error {
	return c.Send(&tele.Document{
		File:     tele.FromDisk(logger.LogsPath),
		FileName: path.Base(logger.LogsPath),
	})
}
