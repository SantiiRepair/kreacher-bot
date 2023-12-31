package helpers

import (
	"encoding/json"
	"fmt"
)

func YtSearch(query string, opts ...string) (*YtSearchResult, error) {
	var ytsr YtSearchResult
	if len(opts) > 0 {
		stdout, err := Bash(fmt.Sprintf("yt-dlp ytsearch%s:'%s' --dump-json --skip-download --quiet --ignore-errors", opts[0], query))
		if err != nil {
			return nil, err
		}

		if len(stdout) == 0 {
			return nil, nil
		}

		json.Unmarshal([]byte(stdout), &ytsr)
		return &ytsr, nil
	}

	stdout, err := Bash(fmt.Sprintf("yt-dlp ytsearch:'%s' --dump-json --skip-download --quiet --ignore-errors", query))
	if err != nil {
		return nil, err
	}

	if len(stdout) == 0 {
		return nil, nil
	}

	json.Unmarshal([]byte(stdout), &ytsr)
	return &ytsr, nil
}

func YtDownloader(format string, link string) error {
	_, err := Bash(fmt.Sprintf("yt-dlp -g -f '%s' %s", format, link))
	if err != nil {
		return err
	}

	return nil
}

type YtSearchResult struct {
	LiveStatus           string                 `json:"live_status"`
	ReleaseTimestamp     string                 `json:"release_timestamp"`
	FormatSortFields     []interface{}          `json:"_format_sort_fields"`
	AutomaticCaptions    map[string]interface{} `json:"automatic_captions"`
	Subtitles            map[string]interface{} `json:"subtitles"`
	CommentCount         int                    `json:"comment_count"`
	Chapters             interface{}            `json:"chapters"`
	Heatmap              interface{}            `json:"heatmap"`
	LikeCount            int                    `json:"like_count"`
	Channel              string                 `json:"channel"`
	ChannelFollowerCount int                    `json:"channel_follower_count"`
	Uploader             string                 `json:"uploader"`
	UploaderID           string                 `json:"uploader_id"`
	UploaderURL          string                 `json:"uploader_url"`
	UploadDate           string                 `json:"upload_date"`
	Availability         string                 `json:"availability"`
	OriginalURL          string                 `json:"original_url"`
	WebpageURLBasename   string                 `json:"webpage_url_basename"`
	WebpageURLDomain     string                 `json:"webpage_url_domain"`
	Extractor            string                 `json:"extractor"`
	ExtractorKey         string                 `json:"extractor_key"`
	PlaylistCount        int                    `json:"playlist_count"`
	Playlist             string                 `json:"playlist"`
	PlaylistID           string                 `json:"playlist_id"`
	PlaylistTitle        string                 `json:"playlist_title"`
	PlaylistUploader     interface{}            `json:"playlist_uploader"`
	PlaylistUploaderID   interface{}            `json:"playlist_uploader_id"`
	NEntries             int                    `json:"n_entries"`
	PlaylistIndex        int                    `json:"playlist_index"`
	LastPlaylistIndex    int                    `json:"__last_playlist_index"`
	PlaylistAutonumber   int                    `json:"playlist_autonumber"`
	DisplayID            string                 `json:"display_id"`
	Fulltitle            string                 `json:"fulltitle"`
	DurationString       string                 `json:"duration_string"`
	ReleaseYear          interface{}            `json:"release_year"`
	IsLive               bool                   `json:"is_live"`
	WasLive              bool                   `json:"was_live"`
	RequestedSubtitles   interface{}            `json:"requested_subtitles"`
	HasDrm               interface{}            `json:"_has_drm"`
	Epoch                int                    `json:"epoch"`
	RequestedFormats     []interface{}          `json:"requested_formats"`
	Format               string                 `json:"format"`
	FormatID             string                 `json:"format_id"`
	Ext                  string                 `json:"ext"`
	Protocol             string                 `json:"protocol"`
	Language             string                 `json:"language"`
	FormatNote           string                 `json:"format_note"`
	FilesizeApprox       int                    `json:"filesize_approx"`
	Tbr                  float64                `json:"tbr"`
	Width                int                    `json:"width"`
	Height               int                    `json:"height"`
	Resolution           string                 `json:"resolution"`
	Fps                  float64                `json:"fps"`
	DynamicRange         string                 `json:"dynamic_range"`
	Vcodec               string                 `json:"vcodec"`
	Vbr                  float64                `json:"vbr"`
	StretchedRatio       interface{}            `json:"stretched_ratio"`
	AspectRatio          float64                `json:"aspect_ratio"`
	Acodec               string                 `json:"acodec"`
	Abr                  float64                `json:"abr"`
	Asr                  int                    `json:"asr"`
	AudioChannels        int                    `json:"audio_channels"`
	Filename             string                 `json:"filename"`
	Type                 string                 `json:"_type"`
	Version              map[string]interface{} `json:"_version"`
}
