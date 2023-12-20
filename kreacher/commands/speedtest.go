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
	if st != nil {
		c.Delete()
		caption := fmt.Sprintf("<b>Speedtest Results\n\nClient:</b>\n<b><i>ISP:</i></b> %s\n<b><i>Country:</i></b> %s\n\n<b><i>Server:</i></b>\n<b><i>Name:</i></b> %s\n<b><i>Country:</i></b> %s\n<b><i>Sponsor:</i></b> %s\n<b><i>Latency:</i></b> %s\n<b><i>Ping:</i></b> %s",
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

	err = c.Send("<b><i>The speedtest could not be performed</i></b>", tele.ParseMode(tele.ModeHTML))

	return err
}
