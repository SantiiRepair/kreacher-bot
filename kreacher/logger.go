package kreacher

import (
	"log"
	"log/syslog"
)

func NewLogger() *log.Logger {
	var logger *log.Logger

	syslogWriter, err := syslog.New(syslog.LOG_INFO, "my-app")
	if err != nil {
		log.Fatal(err)
	}
	logger.SetOutput(syslogWriter)
	logger.SetFlags(0)

	return logger
}
