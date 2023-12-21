package commands

import (
	"fmt"
	"strings"

	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/helpers"
)

func Shell(c tele.Context) error {
	cmd := strings.Join(c.Args(), " ")

	stdout, err := helpers.Bash(cmd)

	if err != nil {
		text := fmt.Sprintf("```shell\n%s\n```", err)
		err = c.Send(text, tele.ParseMode(tele.ModeMarkdownV2))

		return err
	}

	if stdout != "" {
		text := fmt.Sprintf("```shell\n%s\n```", stdout)
		err = c.Send(text, tele.ParseMode(tele.ModeMarkdownV2))

		return err
	}

	err = c.Send("<b><i>Master, stdout is empty.</i></b>", tele.ParseMode(tele.ModeHTML))

	return err
}
