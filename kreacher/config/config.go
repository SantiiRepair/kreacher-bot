package config

import (
	"log"
	"os"
	"path"
	"strconv"

	"github.com/joho/godotenv"
)

func init() {
	err := godotenv.Load(path.Join("..", ".env"))
	if err != nil {
		log.Fatalf("No .env file found")
	}
}

func BotConfig() *TBotConfig {

	apiID, _ := strconv.Atoi(os.Getenv("API_ID"))
	apiHash := os.Getenv("API_HASH")
	botToken := os.Getenv("BOT_TOKEN")
	channel := os.Getenv("CHANNEL")
	esMoviesChannel := os.Getenv("ES_MOVIES_CHANNEL")
	esSeriesChannel := os.Getenv("ES_SERIES_CHANNEL")
	managementMode := os.Getenv("MANAGEMENT_MODE")
	maintainer := os.Getenv("MAINTAINER")
	postgresDB := os.Getenv("POSTGRES_DB")
	postgresUser := os.Getenv("POSTGRES_USER")
	postgressPassword := os.Getenv("POSTGRES_PASSWORD")
	postgresHost := os.Getenv("POSTGRES_HOST")
	postgresPort, _ := strconv.Atoi(os.Getenv("POSTGRES_PORT"))
	redisHost := os.Getenv("REDIS_HOST")
	redisPassword := os.Getenv("REDIS_PASSWORD")
	redisPort, _ := strconv.Atoi(os.Getenv("REDIS_PORT"))

	return &TBotConfig{
		APIID:            apiID,
		APIHash:          apiHash,
		BotToken:         botToken,
		Channel:          channel,
		ESMoviesChannel:  esMoviesChannel,
		ESSeriesChannel:  esSeriesChannel,
		ManagementMode:   managementMode,
		Maintainer:       maintainer,
		PostgresDB:       postgresDB,
		PostgresUser:     postgresUser,
		PostgresPassword: postgressPassword,
		PostgresHost:     postgresHost,
		PostgresPort:     postgresPort,
		RedisHost:        redisHost,
		RedisPassword:    redisPassword,
		RedisPort:        redisPort,
	}
}
