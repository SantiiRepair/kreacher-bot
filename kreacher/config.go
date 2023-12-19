package kreacher

import (
	"fmt"
	"os"

	"github.com/joho/godotenv"
)

type Config struct {
	APIID            string
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
	PostgresPort     string
	RedisHost        string
	RedisPassword    string
	RedisPort        string
}

func NewConfig() *Config {
	err := godotenv.Load("../.env")
	if err != nil {
		fmt.Println("No .env file found")
	}

	return &Config{
		APIID:            os.Getenv("API_ID"),
		APIHash:          os.Getenv("API_HASH"),
		BotToken:         os.Getenv("BOT_TOKEN"),
		BotUsername:      os.Getenv("BOT_USERNAME"),
		Channel:          os.Getenv("CHANNEL"),
		ESMoviesChannel:  os.Getenv("ES_MOVIES_CHANNEL"),
		ESSeriesChannel:  os.Getenv("ES_SERIES_CHANNEL"),
		ManagementMode:   os.Getenv("MANAGEMENT_MODE"),
		Maintainer:       os.Getenv("MANTAINER"),
		SessionString:    os.Getenv("SESSION_STRING"),
		PostgresDB:       os.Getenv("POSTGRES_DB"),
		PostgresUser:     os.Getenv("POSTGRES_USER"),
		PostgresPassword: os.Getenv("POSTGRES_PASSWORD"),
		PostgresHost:     os.Getenv("POSTGRES_HOST"),
		PostgresPort:     os.Getenv("POSTGRES_PORT"),
		RedisHost:        os.Getenv("REDIS_HOST"),
		RedisPassword:    os.Getenv("REDIS_PASSWORD"),
		RedisPort:        os.Getenv("REDIS_PORT"),
	}
}
