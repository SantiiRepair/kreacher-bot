package helpers

import (
	"fmt"
	"io"
	"os"
	"path"

	uuid "github.com/google/uuid"
	ini "gopkg.in/ini.v1"
)

func TTS(text string, opts ...string) (string, error) {
	tempFile, err := os.Create(fmt.Sprintf("%s.txt", uuid.New()))

	if err != nil {
		return "", err
	}

	_, err = io.WriteString(tempFile, text)

	if err != nil {
		return "", err
	}

	err = tempFile.Sync()

	if err != nil {
		return "", err
	}

	cfg, err := ini.Load("")

	if err != nil {
		return "", err
	}

	ast := cfg.Section("ADVANCED")

	piperPathKey, err := ast.GetKey("PIPER_DATA_PATH")

	if err != nil {
		return "", err
	}

	tempPathKey, err := ast.GetKey("TEMP_PATH")

	if err != nil {
		return "", err
	}

	piperModelsPath := path.Join(piperPathKey.String(), "models")

	_, err = os.Stat(piperModelsPath)

	if os.IsNotExist(err) {
		os.MkdirAll(piperModelsPath, 0755)
	}

	outputFile := path.Join(tempPathKey.String(), "tts", fmt.Sprintf("%s.wav", uuid.New()))

	_, err = os.Stat(path.Base(outputFile))

	if os.IsNotExist(err) {
		os.MkdirAll(outputFile, 0755)
	}

	stdout, err := Bash(fmt.Sprintf(
		"piper -m %s --download-dir %s --data-dir %s -f %s < %s",
		"",
		piperModelsPath,
		piperModelsPath,
		outputFile,
		tempFile.Name(),
	))

	if err != nil {
		return "", err
	}

	err = os.Remove(tempFile.Name())

	if err != nil {
		return "", err
	}

	return stdout, nil

}
