package helpers

type SourceType int
type MediaType string

type queue struct {
	Requester     int64  `json:"requester"`
	AudioStream   string `json:"audio_stream"`
	VideoStream   string `json:"video_stream"`
	NumberInQueue int    `json:"number_in_queue"`
}

type Queue struct {
	Requester   int64  `json:"requester"`
	AudioStream string `json:"audio_stream"`
	VideoStream string `json:"video_stream"`
}
