package commands

import (
	"fmt"
	"strconv"

	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/helpers"
)

func Speedtest(c tele.Context) error {
	msg, err := c.Bot().Send(c.Recipient(), "<b><i>Kreacher is here to serve you.\n\nRunning Speedtest...</i></b> 📶", tele.ParseMode(tele.ModeHTML))
	
	if err != nil {
		return err
	}

	mdb := tele.StoredMessage{ChatID: msg.Chat.ID, MessageID: strconv.Itoa(msg.ID)}
	
	st, err := helpers.Speedtest()

	if err != nil {
		return err
	}

	if st.Share != "" {

		c.Bot().Delete(&mdb)

		caption := fmt.Sprintf("<b>Speedtest Results\n\nClient:</b>\n<b><i>ISP:</i></b> %s\n<b><i>Country:</i></b> %s\n\n<b><i>Server:</i></b>\n<b><i>Name:</i></b> %s\n<b><i>Country:</i></b> %s\n<b><i>Sponsor:</i></b> %s\n<b><i>Latency:</i></b> %.2f\n<b><i>Ping:</i></b> %.2f",
			st.Client.ISP,
			st.Client.Country,
			st.Server.Name,
			st.Server.Country,
			st.Server.Sponsor,
			st.Server.Latency,
			st.Ping,
		)

		photo := &tele.Photo{
			File: tele.FromURL(st.Share),
			Caption: caption,
		}

		err = c.Send(photo, tele.ParseMode(tele.ModeHTML))

		return err
	}

	err = c.Send("<b><i>The speedtest could not be performed</i></b>", tele.ParseMode(tele.ModeHTML))

	return err
}
