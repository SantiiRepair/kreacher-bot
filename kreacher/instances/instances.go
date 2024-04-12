package instances

import (
	"context"
	"fmt"
	"os/exec"
	"time"

	tg "github.com/amarnathcjd/gogram/telegram"
	"github.com/fatih/color"
	pgx "github.com/jackc/pgx/v5"
	redis "github.com/redis/go-redis/v9"
	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/config"
	"santiirepair.dev/kreacher/logger"
	n "santiirepair.dev/kreacher/ntgcalls"
)

func init() {

	var err error

	_, err = exec.LookPath("yt-dlp")
	if err != nil {
		panic("yt-dlp isn't installed")
	}

	_, err = exec.LookPath("speedtest")
	if err != nil {
		panic("speedtest isn't installed")
	}

	N = n.NTgCalls()

	B, err = tele.NewBot(tele.Settings{
		Token:  config.BotConfig().BotToken,
		Poller: &tele.LongPoller{Timeout: 10 * time.Second},
		OnError: func(err error, ctx tele.Context) {
			logger.Error(err.Error())
		},
	})

	if err != nil {
		panic(err)
	}

	defer B.Close()
	CY.Printf("✔️ Bot client connected to %s", B.URL)

	U, err = tg.NewClient(tg.ClientConfig{
		AppID:    int32(config.BotConfig().APIID),
		AppHash:  config.BotConfig().APIHash,
		Session:  ".mtproto",
		LogLevel: tg.LogDisable,
	})

	if err != nil {
		panic(err)
	}

	U.Start()
	CY.Println("\n✔️ Initialized new MTProto client, waiting to connect...")

	R = redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%d", config.BotConfig().RedisHost, config.BotConfig().RedisPort),
		Password: config.BotConfig().RedisPassword,
		DB:       0, // use default DB
		Protocol: 3, // specify 2 for RESP 2 or 3 for RESP 3
	})

	_, err = R.Ping(context.Background()).Result()
	if err != nil {
		panic(err)
	}

	CY.Print("✔️ Redis client connected, waiting for requests...")

	/*
		dbUrl := fmt.Sprintf("postgres://%s:%s@%s:%d/%s",
			BotConfig().PostgresUser,
			BotConfig().PostgresPassword,
			BotConfig().PostgresHost,
			BotConfig().PostgresPort,
			BotConfig().PostgresDB,
		)

		idbc, err := pgx.Connect(ctx, dbUrl)

		if err != nil {
			panic(err)
		}

		defer idbc.Close(ctx)
		cy.Println("\n✔️ PGX client connected to PostgreSQL database, waiting for requests...")
	*/

	// Set client instances to late vars in vars.go file.
}

var (
	B *tele.Bot
	U *tg.Client
	R *redis.Client
	D *pgx.Conn
	N *n.Client
	CY = color.New(color.FgCyan)
)
