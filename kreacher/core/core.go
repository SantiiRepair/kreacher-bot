package core

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"time"

	pebbledb "github.com/cockroachdb/pebble"
	boltstor "github.com/gotd/contrib/bbolt"
	"github.com/gotd/contrib/middleware/floodwait"
	"github.com/gotd/contrib/middleware/ratelimit"
	"github.com/gotd/contrib/pebble"
	"github.com/gotd/contrib/storage"
	"github.com/gotd/td/telegram"
	"github.com/gotd/td/telegram/auth"
	"github.com/gotd/td/telegram/query"
	"github.com/gotd/td/telegram/updates"
	"github.com/gotd/td/tg"
	pgx "github.com/jackc/pgx/v5"
	"github.com/pkg/errors"
	redis "github.com/redis/go-redis/v9"
	"go.etcd.io/bbolt"
	"go.uber.org/zap"
	"golang.org/x/time/rate"
	tele "gopkg.in/telebot.v3"

	"santiirepair.dev/kreacher/config"
	"santiirepair.dev/kreacher/logger"
	"santiirepair.dev/kreacher/ntgcalls"
)

func init() {

	var err error

	N = ntgcalls.NTgCalls()

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
	fmt.Printf("✔️ Bot client connected to %s", B.URL)

	sessionDir := filepath.Join("..", "session")
	if err := os.MkdirAll(sessionDir, 0700); err != nil {
		panic(err)
	}

	sessionStorage := &telegram.FileSessionStorage{
		Path: filepath.Join(sessionDir, "session.json"),
	}

	// Peer storage, for resolve caching and short updates handling.
	db, err := pebbledb.Open(filepath.Join(sessionDir, "peers.pebble.db"), &pebbledb.Options{})
	if err != nil {
		panic(err)
	}

	PDB = pebble.NewPeerStorage(db)
	logger.Info("storage", zap.String("path", sessionDir))

	// Setting up client.
	//
	// Dispatcher is used to register handlers for events.
	dispatcher := tg.NewUpdateDispatcher()
	// Setting up update handler that will fill peer storage before
	// calling dispatcher handlers.
	updateHandler := storage.UpdateHook(dispatcher, PDB)

	// Setting up persistent storage for qts/pts to be able to
	// recover after restart.
	boltdb, err := bbolt.Open(filepath.Join(sessionDir, "updates.bolt.db"), 0666, nil)
	if err != nil {
		panic(err)
	}

	updatesRecovery := updates.New(updates.Config{
		Handler: updateHandler, // using previous handler with PDB
		Logger:  logger.T.Named("updates.recovery"),
		Storage: boltstor.NewStateStorage(boltdb),
	})

	waiter := floodwait.NewWaiter().WithCallback(func(ctx context.Context, wait floodwait.FloodWait) {
		// Notifying about flood wait.
		logger.Warn("flood wait", zap.Duration("wait", wait.Duration))
	})

	U = telegram.NewClient(config.BotConfig().APIID, config.BotConfig().APIHash, telegram.Options{
		Logger:         logger.T,        // Passing logger for observability.
		SessionStorage: sessionStorage,  // Setting up session sessionStorage to store auth data.
		UpdateHandler:  updatesRecovery, // Setting up handler for updates from server.
		Middlewares: []telegram.Middleware{
			// Setting up FLOOD_WAIT handler to automatically wait and retry request.
			waiter,
			// Setting up general rate limits to less likely get flood wait errors.
			ratelimit.New(rate.Every(time.Millisecond*100), 5),
		},
	})

	go func() {
		waiter.Run(context.Background(), func(ctx context.Context) error {
			// Spawning main goroutine.
			if err := U.Run(ctx, func(ctx context.Context) error {
				flow := auth.NewFlow(terminal{}, auth.SendCodeOptions{})
				if err := U.Auth().IfNecessary(ctx, flow); err != nil {
					return errors.Wrap(err, "auth")
				}

				// Getting info about current user.
				self, err := U.Self(context.Background())
				if err != nil {
					panic(err)
				}

				name := self.FirstName
				if self.Username != "" {
					// Username is optional.
					name = fmt.Sprintf("%s (@%s)", name, self.Username)
				}

				fmt.Printf("\n✔️ Initialized new MTProto client, %s\n", name)

				logger.Info("login",
					zap.String("first_name", self.FirstName),
					zap.String("last_name", self.LastName),
					zap.String("username", self.Username),
					zap.Int64("id", self.ID),
				)

				logger.Info("filling peer storage from dialogs to cache entities")
				collector := storage.CollectPeers(PDB)
				if err := collector.Dialogs(ctx, query.GetDialogs(U.API()).Iter()); err != nil {
					return errors.Wrap(err, "collect peers")
				}

				return updatesRecovery.Run(ctx, U.API(), self.ID, updates.AuthOptions{
					IsBot: self.Bot,
					OnStart: func(ctx context.Context) {
						logger.Info("update recovery initialized and started, listening for events")
					},
				})
			}); err != nil {
				return errors.Wrap(err, "run")
			}

			return nil
		})
	}()

	time.Sleep(2 * time.Second)

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

	fmt.Print("✔️ Redis client connected, waiting for requests...\n")

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
		fmt.Println("\n✔️ PGX client connected to PostgreSQL database, waiting for requests...")
	*/

}

var (
	B   *tele.Bot
	U   *telegram.Client
	R   *redis.Client
	D   *pgx.Conn
	N   *ntgcalls.Client
	S   = time.Now()
	PDB = &pebble.PeerStorage{}
)
