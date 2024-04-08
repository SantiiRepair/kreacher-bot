package helpers

import (
	"bytes"
	"errors"
	"os/exec"
	"strings"
)

func Shell(args ...string) (*bytes.Buffer, error) {
	var outBytes, errBytes bytes.Buffer

	cmd := exec.Command(args[0], args[1:]...)
	cmd.Stdout = &outBytes
	cmd.Stderr = &errBytes

	err := cmd.Run()
	if err != nil {
		return nil, err
	}

	if errBytes.Len() > 0 {
		return nil, errors.New(strings.TrimSpace(errBytes.String()))
	}

	return &outBytes, nil
}
