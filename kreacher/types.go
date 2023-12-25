package main

import (
	"database/sql"

	td "github.com/gotd/td/telegram"
	redis "github.com/redis/go-redis/v9"
	tele "gopkg.in/telebot.v3"
)

// Custom logger set config for entire bot.
type Logger struct {
	Name string
	Path string
}

// MTProto basic params.
type MTProto struct {
	APIID   int
	APIHash string
	Options *td.Options
}

// Database SQL params.
type DB struct {
	DriverName string
	DriverConn string
}

type BotParams struct {
	Bot     *tele.Settings
	UserBot *MTProto
	RedisDB *redis.Options
	DB      *DB
}

type BotContext struct {
	Bot     *tele.Bot
	UserBot *td.Client
	RedisDB *redis.Client
	DB      *sql.DB
}

type botConfigAdvanced struct {
	LogsPath      string
	PiperDataPath string
	TempPath      string
}

type botConfig struct {
	Advanced         *botConfigAdvanced
	ProjectName      string
	APIID            int
	APIHash          string
	BotToken         string
	Channel          string
	ESMoviesChannel  string
	ESSeriesChannel  string
	ManagementMode   string
	Maintainer       string
	PostgresDB       string
	PostgresUser     string
	PostgresPassword string
	PostgresHost     string
	PostgresPort     int
	RedisHost        string
	RedisPassword    string
	RedisPort        int
}
