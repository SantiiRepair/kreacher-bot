package main

import (
	"github.com/fatih/color"
	pgx "github.com/jackc/pgx/v5"
	tele "gopkg.in/telebot.v3"

	td "github.com/gotd/td/telegram"
	redis "github.com/redis/go-redis/v9"
)

var (
	bot  *tele.Bot
	ubot *td.Client
	rdc  *redis.Client
	dbc  *pgx.Conn
	// Cyan colored initial instance.
	cy = color.New(color.FgCyan)
)
