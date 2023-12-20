package commands

import (
	"fmt"

	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/helpers"
)

func Speedtest(c tele.Context) error {
	err := c.Send("<b><i>Kreacher is here to serve you.\n\nRunning Speedtest...</i></b> 📶", tele.ParseMode(tele.ModeHTML))
  
	if err != nil {
		return err
	}

	st := helpers.Speedtest()
  c.Delete()

	caption := fmt.Sprintf("<b>Speedtest Results\n\nClient</b>:\n<b><i>ISP: %s\nCountry: %s\n\nServer:\nName: %s\nCountry: %s\nSponsor: %s\nLatency: %s\nPing: %s</i></b>",
		"",
    st.Country,
    st.Name,
    st.Country, 
    st.Sponsor,
    st.Latency,
    st.TestDuration.Ping,
  )

  err = c.Send(caption, tele.ParseMode(tele.ModeHTML))
  
	return err
}
