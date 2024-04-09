package main

// Custom logger set config for entire bot.
type Logger struct {
	Name string
	Path string
}

// Database SQL params.
type DB struct {
	DriverName string
	DriverConn string
}

type botConfig struct {
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
