package commands

import (
	"fmt"
	"strconv"

	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/helpers"
)

func speedtest(c tele.Context) error {
	msg, err := c.Bot().Send(c.Recipient(), stStarted, tele.ParseMode(tele.ModeHTML))

	if err != nil {
		return err
	}

	storedMessage := tele.StoredMessage{ChatID: msg.Chat.ID, MessageID: strconv.Itoa(msg.ID)}
	defer c.Bot().Delete(&storedMessage)

	st, err := helpers.Speedtest()
	if err != nil {
		return c.Send("*_A problem occurred running the speedtest_*", tele.ParseMode(tele.ModeMarkdownV2))
	}

	if st.Share != "" {
		caption := fmt.Sprintf(
			stResult,
			st.Client.ISP,
			st.Client.Country,
			st.Server.Name,
			st.Server.Country,
			st.Server.Sponsor,
			st.Server.Latency,
			st.Ping,
		)

		photo := &tele.Photo{
			File:    tele.FromURL(st.Share),
			Caption: caption,
		}

		return c.Send(photo, tele.ParseMode(tele.ModeHTML))
	}

	return c.Send(stErr, tele.ParseMode(tele.ModeHTML))
}

var stStarted = `
<b><i>Kreacher is here to serve you.</i></b>

<b><i>Running Speedtest...</i></b> 📶
`

var stResult = `
<b>Speedtest Result</b>

<b>Client:</b>
<b><i>ISP:</i></b> %s
<b><i>Country:</i></b> %s

<b>Server:</b>
<b><i>Name:</i></b> %s
<b><i>Country:</i></b> %s
<b><i>Sponsor:</i></b> %s
<b><i>Latency:</i></b> %.2f
<b><i>Ping:</i></b> %.2f
`

var stErr = "<b><i>The speedtest could not be performed</i></b>"
