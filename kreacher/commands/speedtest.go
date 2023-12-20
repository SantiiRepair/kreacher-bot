package commands

import (
	"fmt"

	tele "gopkg.in/telebot.v3"
)

func Speedtest(c tele.Context) (error) {
	err := c.Send("**__Kreacher is here to serve you.\nRunning Speedtest...__** 📶")

    if err != nil {
        return err
    }

    fmt.Sprintf("**Speedtest Results**\n\n**Client**:\n**__ISP__**: %s\n**__Country__**: %s\n\n**Server**:\n**__Name__**: %s\n**__Country:__** %s\n**__Sponsor:__** %s\n**__Latency__**: %s\n**__Ping__**: %s",
		clientISP, clientCountry, serverName, serverCountry, serverSponsor, latency, ping)
    
    return err
}