package internal

import (
	"encoding/json"
	"os/exec"
)

type MediaType int

const (
	AUDIO MediaType = iota
	VIDEO
	UNKNOWN
)

func checkMediaType(filePath string) (MediaType, error) {
	cmd := exec.Command("ffprobe", "-loglevel", "error", "-show_entries", "stream=codec_type", "-of", "json", filePath)
	output, err := cmd.Output()
	if err != nil {
		return UNKNOWN, err
	}

	var result map[string]interface{}
	if err := json.Unmarshal(output, &result); err != nil {
		return UNKNOWN, err
	}

	streams, ok := result["streams"].([]interface{})
	if !ok || len(streams) == 0 {
		return UNKNOWN, nil
	}

	for _, stream := range streams {
		streamMap := stream.(map[string]interface{})
		if codecType, exists := streamMap["codec_type"]; exists {
			if codecType == "video" {
				return VIDEO, nil
			} else if codecType == "audio" {
				return AUDIO, nil
			}
		}
	}

	return UNKNOWN, nil
}
