package main

import (
	"database/sql"

	"github.com/fatih/color"
	tele "gopkg.in/telebot.v3"

	td "github.com/gotd/td/telegram"
	redis "github.com/redis/go-redis/v9"
)

var (
	bot  *tele.Bot
	ubot *td.Client
	rdc  *redis.Client
	db   *sql.DB
	// Cyan colored initial instance for real.
	cy = color.New(color.FgCyan).Add(color.Underline)
)
