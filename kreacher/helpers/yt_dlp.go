package helpers

import (
	"encoding/json"
	"fmt"
	"strings"
)

func GetYoutubeStream(link string) (string, string, error) {
	stdout, stderr := Bash("yt-dlp", "-g", "-f", "bestvideo+bestaudio/best", link)
	if stderr != nil {
		return "", "", stderr
	}

	output := stdout.String()
	lines := strings.Split(output, "\n")
	if len(lines) < 2 {
		return "", "", fmt.Errorf("expected at least 2 lines of output, got %d", len(lines))
	}

	audioLink := lines[0]
	videoLink := lines[1]
	return audioLink, videoLink, nil
}

func YoutubeSearch(query string, mediaType MediaType, searchRange ...string) (*YoutubeSearchResult, error) {
	var result YoutubeSearchResult
	args := make([]string, 0)

	args = append(args, "yt-dlp")

	if len(searchRange) > 0 {
		args = append(args, fmt.Sprintf("ytsearch%s:'%s'", searchRange[0], query))
	} else {
		args = append(args, fmt.Sprintf("ytsearch:'%s'", query))
	}

	args = append(args, "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best", "--get-title", "--get-url", "--get-format")

	stdout, err := Bash(args...)
	if err != nil {
		return nil, err
	}

	k := strings.Split(stdout.String(), "\n")

	mb, err := json.Marshal(
		map[string]string{
			"title":     k[0],
			"audio_url": k[2],
			"video_url": k[1],
			"format":    k[3],
		})

	if err != nil {
		return nil, err
	}

	json.Unmarshal(mb, &result)
	return &result, nil
}

func YoutubeDownloader(format string, link string) error {
	_, err := Bash("yt-dlp", "-g", "-f", fmt.Sprintf("'%s' %s", format, link))
	if err != nil {
		return err
	}

	return nil
}

type YoutubeSearchResult struct {
	Title    string `json:"title"`
	AudioURL string `json:"audio_url"`
	VideoURL string `json:"video_url"`
	Format   string `json:"format"`
}
