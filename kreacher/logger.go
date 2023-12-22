package main

import (
	"github.com/sirupsen/logrus"
	"io"
	"log"
	"os"
)

var (
	lg *logrus.Logger
)

func init() {
	file, err := os.OpenFile(botConfig().LogFilePath, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)

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

var (

	// ConfigError ...
	ConfigError = "%v type=config.error"

	// HTTPError ...
	HTTPError = "%v type=http.error"

	// HTTPWarn ...
	HTTPWarn = "%v type=http.warn"

	// HTTPInfo ...
	HTTPInfo = "%v type=http.info"
)
