package kreacher

import (
	"log"
	"os"
)

func NewLogger(name string, path string) (*log.Logger, error) {
	var logger *log.Logger
	file, err := os.OpenFile(path, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	if err != nil {
		return nil, err
	}

	defer file.Close()

	logger.SetOutput(file)
	logger.SetFlags(0)

	return logger, nil
}
