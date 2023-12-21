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

	st, err := helpers.Speedtest()

	if err != nil {
		return err
	}

	if st != nil {

		c.Delete()

		caption := fmt.Sprintf("<b>Speedtest Results\n\nClient:</b>\n<b><i>ISP:</i></b> %s\n<b><i>Country:</i></b> %s\n\n<b><i>Server:</i></b>\n<b><i>Name:</i></b> %s\n<b><i>Country:</i></b> %s\n<b><i>Sponsor:</i></b> %s\n<b><i>Latency:</i></b> %.2f\n<b><i>Ping:</i></b> %.2f",
			st.Client.Country,
			st.Client.ISP,
			st.Server.Name,
			st.Server.Country,
			st.Server.Sponsor,
			st.Server.Latency,
			st.Ping,
		)

		err = c.Send(caption, tele.ParseMode(tele.ModeHTML))

		return err
	}

	err = c.Send("<b><i>The speedtest could not be performed</i></b>", tele.ParseMode(tele.ModeHTML))

	return err
}
