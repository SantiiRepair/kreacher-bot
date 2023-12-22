package main

import (
	"fmt"
	"os"
	"strconv"

	"github.com/joho/godotenv"
)

func botConfig() *BotConfig {
	err := godotenv.Load("../.env")
	if err != nil {
		fmt.Println("No .env file found")
	}

	projectName := os.Getenv("PROJECT_NAME")
	apiID, _ := strconv.Atoi(os.Getenv("API_ID"))
	apiHash := os.Getenv("API_HASH")
	botToken := os.Getenv("BOT_TOKEN")
	channel := os.Getenv("CHANNEL")
	esMoviesChannel := os.Getenv("ES_MOVIES_CHANNEL")
	esSeriesChannel := os.Getenv("ES_SERIES_CHANNEL")
	logFilePath := os.Getenv("LOG_FILE_PATH")
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

	return &BotConfig{
		ProjectName:      projectName,
		APIID:            apiID,
		APIHash:          apiHash,
		BotToken:         botToken,
		Channel:          channel,
		ESMoviesChannel:  esMoviesChannel,
		ESSeriesChannel:  esSeriesChannel,
		LogFilePath:      logFilePath,
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
