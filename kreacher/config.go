package main

import (
	ini "gopkg.in/ini.v1"
	"log"
	"os"
	"strconv"

	"github.com/joho/godotenv"
)

func init() {
	err := godotenv.Load("../.env")
	if err != nil {
		log.Fatalf("No .env file found")
	}
}

func BotConfig() *botConfig {
	cfg, err := ini.Load("../kreacher.cfg")

	if err != nil {
		log.Fatalf("error loading cfg file: %v", err)
	}

	ast := cfg.Section("ADVANCED")

	logsPathKey, err := ast.GetKey("LOGS_PATH")

	if err != nil {
		log.Fatalf("error getting LOGS_PATH value: %v", err)
	}

	piperDataPathKey, err := ast.GetKey("PIPER_DATA_PATH")

	if err != nil {
		log.Fatalf("error getting PIPER_DATA_PATH value: %v", err)
	}

	tempPathKey, err := ast.GetKey("TEMP_PATH")

	if err != nil {
		log.Fatalf("error getting TEMP_PATH value: %v", err)
	}

	advanced := &botConfigAdvanced{
		LogsPath:      logsPathKey.String(),
		PiperDataPath: piperDataPathKey.String(),
		TempPath:      tempPathKey.String(),
	}

	projectName := os.Getenv("PROJECT_NAME")
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

	return &botConfig{
		Advanced:         advanced,
		ProjectName:      projectName,
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
