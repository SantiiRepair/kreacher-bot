package helpers

import (
	"net/url"
	"regexp"
)

const (
	YoutubeURL SourceType = iota
	CommonURL
	NotURL
)

const (
	Audio MediaType = "audio"
	Video MediaType = "video"
)

func GetURLType(s string) SourceType {
	if isYouTubeURL(s) {
		return YoutubeURL
	} else if isURL(s) {
		return CommonURL
	}

	return NotURL
}

func isYouTubeURL(s string) bool {
	re := regexp.MustCompile(`^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+`)
	return re.MatchString(s)
}

func isURL(s string) bool {
	u, err := url.Parse(s)
	if err != nil || u.Scheme == "" || u.Host == "" {
		return false
	}
	return true
}
