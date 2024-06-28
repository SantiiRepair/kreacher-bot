package logger

import (
	"fmt"
	"os"
	"path"

	"github.com/sirupsen/logrus"
)

var log = logrus.New()
var LogsPath = path.Join("..", "logs", "bot.log")

func init() {
	file, err := os.OpenFile(LogsPath, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0666)

	if err != nil {
		panic(fmt.Sprintf("error opening file: %v", err))
	}

	log.SetReportCaller(true)
	log.SetOutput(file)
}

// Info logger, redirect info to log file.
func Info(format string, v ...interface{}) {
	log.Infof(format, v...)
}

// Warn logger, redirect warning to log file.
func Warn(format string, v ...interface{}) {
	log.Warnf(format, v...)
}

// Error logger, redirect error to log file.
func Error(format error, v ...interface{}) {
	log.Errorf(format.Error(), v...)
}
