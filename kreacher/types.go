package main

import (
	"database/sql"
	"log"

	td "github.com/gotd/td/telegram"
	redis "github.com/redis/go-redis/v9"
	tele "gopkg.in/telebot.v3"
)

type Logger struct {
	Name string
	Path string
}

type MTProto struct {
	APIID   int
	APIHash string
	Options *td.Options
}

// Database SQL
type DB struct {
	DriverName string
	DriverConn string
}

type KParams struct {
	Logger  *Logger
	Bot     *tele.Settings
	UserBot *MTProto
	RedisDB *redis.Options
	DB      *DB
}

type Kreacher struct {
	Logger  *log.Logger
	Bot     *tele.Bot
	UserBot *td.Client
	RedisDB *redis.Client
	DB      *sql.DB
}

type KConfig struct {
	APIID            int
	APIHash          string
	BotToken         string
	BotUsername      string
	Channel          string
	ESMoviesChannel  string
	ESSeriesChannel  string
	ManagementMode   string
	Maintainer       string
	SessionString    string
	PostgresDB       string
	PostgresUser     string
	PostgresPassword string
	PostgresHost     string
	PostgresPort     int
	RedisHost        string
	RedisPassword    string
	RedisPort        int
}
