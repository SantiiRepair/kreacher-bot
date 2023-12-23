package helpers

import (
	"fmt"
	"os"
	"path"

	ini "gopkg.in/ini.v1"
)

func TTS(text string, outputFile string, opts ...string) (string, error) {
    cfg, err := ini.Load("")

	if err != nil {
		return "", err
	}

    aKey, err := cfg.Section("").GetKey("")

    if err != nil {
		return "", err
	}

	_, err = os.Stat(aKey.String())

	if !os.IsNotExist(err) {
		os.MkdirAll(opts[0], 0755)
	}

	outputFileBase := path.Base(outputFile)
	_, err = os.Stat(outputFileBase)

	if !os.IsNotExist(err) {
		os.MkdirAll(outputFileBase, 0755)
	}

	stdout, err := Bash(fmt.Sprintf(
		"piper -m %s --download-dir %s --data-dir %s -f %s < %s"),
	)

	if err != nil {
		return "", err
	}

	os.Remove()

	return stdout, nil

}
