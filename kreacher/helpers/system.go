package helpers

import (
	"bytes"
	"errors"
	"os/exec"
	"runtime"
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

func GetMemoryUsage() float64 {
	var m runtime.MemStats
	runtime.ReadMemStats(&m)
	totalMemory := float64(m.Alloc + m.Sys)
	usedMemory := float64(m.Alloc)
	result := (usedMemory / totalMemory) * 100

	return result
}
