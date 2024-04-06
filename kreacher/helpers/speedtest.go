package helpers

import (
	"encoding/json"
)

type Client struct {
	IP        string  `json:"ip"`
	Lat       float64 `json:"lat"`
	Lon       float64 `json:"lon"`
	ISP       string  `json:"isp"`
	ISPRating float64 `json:"isprating"`
	Rating    float64 `json:"rating"`
	ISPDLAVG  float64 `json:"ispdlavg"`
	ISPULAVG  float64 `json:"ispulavg"`
	LoggedIn  float64 `json:"loggedin"`
	Country   string  `json:"country"`
}

type Server struct {
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
}

type STResult struct {
	Download      float64 `json:"download"`
	Upload        float64 `json:"upload"`
	Ping          float64 `json:"ping"`
	Server        Server  `json:"server"`
	Timestamp     string  `json:"timestamp"`
	BytesSent     float64 `json:"bytes_sent"`
	BytesReceived float64 `json:"bytes_received"`
	Share         string  `json:"share"`
	Client        Client  `json:"client"`
}

func Speedtest() (*STResult, error) {
	var stresult STResult

	stdout, err := Bash("speedtest", "--json", "--share")

	if err != nil {
		return nil, err
	}

	json.Unmarshal(stdout.Bytes(), &stresult)

	return &stresult, nil
}
