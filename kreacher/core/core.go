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

type noLogger struct{}

func (n *noLogger) Logf(format string, args ...interface{})     {}
func (n *noLogger) Infof(format string, args ...interface{})    {}
func (n *noLogger) Warningf(format string, args ...interface{}) {}
func (n *noLogger) Errorf(format string, args ...interface{})   {}
func (n *noLogger) Fatalf(format string, args ...interface{})   {}
func (n *noLogger) Close()                                      {}

func init() {

	var err error
	N = ntgcalls.NTgCalls()
	B, err = tele.NewBot(tele.Settings{
		URL:    "http://0.0.0.0:8081",
		Token:  config.BotConfig().BotToken,
		Poller: &tele.LongPoller{Timeout: 10 * time.Second},
		OnError: func(err error, ctx tele.Context) {
			logger.Error("gerror", zap.Error(err))
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

	db, err := pebbledb.Open(filepath.Join(sessionDir, "peers.pebble.db"), &pebbledb.Options{Logger: &noLogger{}})
	if err != nil {
		panic(err)
	}

	PDB = pebble.NewPeerStorage(db)
	logger.Info("storage", zap.String("path", sessionDir))

	dispatcher := tg.NewUpdateDispatcher()
	updateHandler := storage.UpdateHook(dispatcher, PDB)

	boltdb, err := bbolt.Open(filepath.Join(sessionDir, "updates.bolt.db"), 0666, nil)
	if err != nil {
		panic(err)
	}

	updatesRecovery := updates.New(updates.Config{
		Handler: updateHandler,
		Logger:  logger.T.Named("updates.recovery"),
		Storage: boltstor.NewStateStorage(boltdb),
	})

	waiter := floodwait.NewWaiter().WithCallback(func(ctx context.Context, wait floodwait.FloodWait) {
		logger.Warn("flood wait", zap.Duration("wait", wait.Duration))
	})

	U = telegram.NewClient(config.BotConfig().APIID, config.BotConfig().APIHash, telegram.Options{
		Logger:         logger.T,
		SessionStorage: sessionStorage,
		UpdateHandler:  updatesRecovery,
		Middlewares: []telegram.Middleware{
			waiter,
			ratelimit.New(rate.Every(time.Millisecond*100), 5),
		},
	})

	var self *tg.User
	uac := make(chan bool)

	go func() {
		waiter.Run(context.Background(), func(ctx context.Context) error {
			if err := U.Run(ctx, func(ctx context.Context) error {
				flow := auth.NewFlow(terminal{}, auth.SendCodeOptions{})
				if err := U.Auth().IfNecessary(ctx, flow); err != nil {
					return errors.Wrap(err, "auth")
				}

				if self, err = U.Self(ctx); err != nil {
					return err
				}

				uac <- true
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

	<-uac
	name := self.FirstName
	if self.Username != "" {
		name = fmt.Sprintf("%s (@%s)", name, self.Username)
	}

	logger.Info("login",
		zap.String("first_name", self.FirstName),
		zap.String("last_name", self.LastName),
		zap.String("username", self.Username),
		zap.Int64("id", self.ID),
	)

	fmt.Printf("\n✔️ Initialized new MTProto client, %s\n", name)

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
