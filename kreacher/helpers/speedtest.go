package helpers

import (
	"encoding/json"
)

func Speedtest() (*SpeedtestResult, error) {
	var speedtestResult SpeedtestResult

	stdout, err := Shell("speedtest", "--json", "--share")

	if err != nil {
		return nil, err
	}

	err = json.Unmarshal(stdout.Bytes(), &speedtestResult)
	if err != nil {
		return nil, err
	}

	return &speedtestResult, nil
}
