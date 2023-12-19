package main

import (
	"io"
	"log"
	"os"
)

func NewLogger(name string, path string) (*log.Logger, error) {
	file, err := os.OpenFile(path, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		return nil, err
	}

	defer file.Close()

	logFile := io.MultiWriter(os.Stdout, file)

	logger := log.New(logFile, name+" ", log.Ldate|log.Ltime|log.Lshortfile)
	logger.SetOutput(logFile)
	logger.SetFlags(0)

	return logger, nil
}
