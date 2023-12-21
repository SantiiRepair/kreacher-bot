package helpers

import (
	"bytes"
	"errors"
	"log"
	"os/exec"
	"strings"
)

func Bash(cmd string) (string, error) {
	var outb, errb bytes.Buffer

	c := exec.Command("bash", "-c", cmd)
	c.Stdout = &outb
	c.Stderr = &errb

	err := c.Run()
	if err != nil {
		log.Println("Error: ", err)
		return "", err
	}

	errStr := errb.String()
	if errStr != "" {
		return "", errors.New(strings.TrimSpace(errStr))
	}

	return outb.String(), nil
}
