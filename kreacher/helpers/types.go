package helpers

type SourceType int
type MediaType string


type Queue struct {
	AudioStream string `json:"audio_strean"`
	VideoStream string `json:"video_strean"`
	Requester string `json:"requester"`
}