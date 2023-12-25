package main

import (
	"io"
	"log"
	"os"

	"github.com/sirupsen/logrus"
)

var (
	lg *logrus.Logger
)

func init() {
	file, err := os.OpenFile(BotConfig().Advanced.LogsPath, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)

	if err != nil {
		log.Fatalf("error opening file: %v", err)
	}

	defer file.Close()

	log := logrus.New()

	log.SetReportCaller(true)

	mw := io.MultiWriter(os.Stdout, file)
	log.SetOutput(mw)
}

// Info logger, redirect info to log file.
func Info(format string, v ...interface{}) {
	lg.Infof(format, v...)
}

// Warn logger, redirect warning to log file.
func Warn(format string, v ...interface{}) {
	lg.Warnf(format, v...)
}

// Error logger, redirect error to log file.
func Error(format string, v ...interface{}) {
	lg.Errorf(format, v...)
}
