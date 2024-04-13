package config

type TBotConfig struct {
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
