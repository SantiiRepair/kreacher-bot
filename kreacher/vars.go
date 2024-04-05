package main

import (
	tg "github.com/amarnathcjd/gogram/telegram"
	"github.com/fatih/color"
	pgx "github.com/jackc/pgx/v5"
	redis "github.com/redis/go-redis/v9"
	tele "gopkg.in/telebot.v3"
	ntgc "santiirepair.dev/kreacher/ntgcalls"
)

var (
	bot      *tele.Bot
	ubot     *tg.Client
	rdc      *redis.Client
	dbc      *pgx.Conn
	ntgcalls *ntgc.Client
	// Cyan colored initial instance.
	cy = color.New(color.FgCyan)
)
