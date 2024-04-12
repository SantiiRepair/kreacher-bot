package commands

import (
	"fmt"
	"strings"

	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/helpers"
)

func sh(c tele.Context) error {
	cmd := strings.Join(c.Args(), " ")

	if cmd == "" {
		err := c.Send(shArgsEmpty, tele.ParseMode(tele.ModeHTML))

		return err
	}

	stdout, err := helpers.Shell(cmd)

	if err != nil {
		text := fmt.Sprintf("```\n%s\n```", err)
		err = c.Send(text, tele.ParseMode(tele.ModeMarkdownV2))

		return err
	}

	if stdout.Len() > 0 {
		text := fmt.Sprintf("```\n%s\n```", stdout)
		err = c.Send(text, tele.ParseMode(tele.ModeMarkdownV2))

		return err
	}

	err = c.Send(shStdoutEmpty, tele.ParseMode(tele.ModeHTML))

	return err
}

var shArgsEmpty = "<b><i>You must provide at least one sh command.</i></b>"

var shStdoutEmpty = "<b><i>Master, stdout is empty.</i></b>"
