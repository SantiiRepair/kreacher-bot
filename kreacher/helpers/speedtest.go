package helpers

import (
	"encoding/json"
)

type Client struct {
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

type SpeedtestResult struct {
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
