package main

import (
	"fmt"
	"os"
	"strconv"

	"github.com/joho/godotenv"
)

func BotConfig() *KConfig {
	err := godotenv.Load("../.env")
	if err != nil {
		fmt.Println("No .env file found")
	}

	apiID, _ := strconv.Atoi(os.Getenv("API_ID"))
	apiHash := os.Getenv("API_HASH")
	botToken := os.Getenv("BOT_TOKEN")
	botUsername := os.Getenv("BOT_USERNAME")
	channel := os.Getenv("CHANNEL")
	esMoviesChannel := os.Getenv("ES_MOVIES_CHANNEL")
	esSeriesChannel := os.Getenv("ES_SERIES_CHANNEL")
	managementMode := os.Getenv("MANAGEMENT_MODE")
	maintainer := os.Getenv("MAINTAINER")
	sessionString := os.Getenv("SESSION_STRING")
	postgresDB := os.Getenv("POSTGRES_DB")
	postgresUser := os.Getenv("POSTGRES_USER")
	postgressPassword := os.Getenv("POSTGRES_PASSWORD")
	postgresHost := os.Getenv("POSTGRES_HOST")
	postgresPort, _ := strconv.Atoi(os.Getenv("POSTGRES_PORT"))
	redisHost := os.Getenv("REDIS_HOST")
	redisPassword := os.Getenv("REDIS_PASSWORD")
	redisPort, _ := strconv.Atoi(os.Getenv("REDIS_PORT"))

	return &KConfig{
		APIID:            apiID,
		APIHash:          apiHash,
		BotToken:         botToken,
		BotUsername:      botUsername,
		Channel:          channel,
		ESMoviesChannel:  esMoviesChannel,
		ESSeriesChannel:  esSeriesChannel,
		ManagementMode:   managementMode,
		Maintainer:       maintainer,
		SessionString:    sessionString,
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
