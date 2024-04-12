package helpers

type SourceType int
type MediaType string

type Queue struct {
	Requester     int64  `json:"requester"`
	AudioSource   string `json:"audio_source"`
	VideoSource   string `json:"video_source"`
	StreamType    string `json:"stream_type"`
	NumberInQueue int    `json:"number_in_queue"`
}

type SpeedtestResult struct {
	Download float64 `json:"download"`
	Upload   float64 `json:"upload"`
	Ping     float64 `json:"ping"`
	Server   struct {
		URL     string  `json:"url"`
		Lat     string  `json:"lat"`
		Lon     string  `json:"lon"`
		Name    string  `json:"name"`
		Country string  `json:"country"`
		CC      string  `json:"cc"`
		Sponsor string  `json:"sponsor"`
		ID      string  `json:"id"`
		Host    string  `json:"host"`
		D       float64 `json:"d"`
		Latency float64 `json:"latency"`
	} `json:"server"`
	Timestamp     string  `json:"timestamp"`
	BytesSent     float64 `json:"bytes_sent"`
	BytesReceived float64 `json:"bytes_received"`
	Share         string  `json:"share"`
	Client        struct {
		IP        string `json:"ip"`
		Lat       string `json:"lat"`
		Lon       string `json:"lon"`
		ISP       string `json:"isp"`
		ISPRating string `json:"isprating"`
		Rating    string `json:"rating"`
		ISPDLAVG  string `json:"ispdlavg"`
		ISPULAVG  string `json:"ispulavg"`
		LoggedIn  string `json:"loggedin"`
		Country   string `json:"country"`
	} `json:"client"`
}

type YoutubeSearchResult struct {
	Title    string `json:"title"`
	AudioURL string `json:"audio_url"`
	VideoURL string `json:"video_url"`
	Format   string `json:"format"`
}
