package callbacks

import (
	"fmt"
	"time"

	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/core"
	"santiirepair.dev/kreacher/helpers"
)

func Start() {
	core.B.Handle(&prevBtn, func(c tele.Context) error {
		chatId := helpers.ParsePeer(c.Chat().ID)
		_, err := helpers.MovePlayList(chatId, "prev")
		if err != nil {}

		return nil
	})

	core.B.Handle(&pauseBtn, func(c tele.Context) error {
		chatId := helpers.ParsePeer(c.Chat().ID)
		core.N.Pause(chatId)

		return c.Edit(c.Message().Text, &tele.ReplyMarkup{
			InlineKeyboard: [][]tele.InlineButton{
				{
					{
						Text:   "⏮",
						Data:   "",
						Unique: "prev",
					},
					{
						Text:   "▶",
						Data:   "",
						Unique: "resume",
					},
					{
						Text:   "⏭️",
						Data:   "",
						Unique: "next",
					},
				},
			},
		})
	})

	core.B.Handle(&resumeBtn, func(c tele.Context) error {
		chatId := helpers.ParsePeer(c.Chat().ID)
		core.N.Resume(chatId)

		return c.Edit(c.Message().Text, &tele.ReplyMarkup{
			InlineKeyboard: [][]tele.InlineButton{
				{
					{
						Text:   "⏮",
						Data:   "",
						Unique: "prev",
					},
					{
						Text:   "⏸️",
						Data:   "",
						Unique: "pause",
					},
					{
						Text:   "⏭️",
						Data:   "",
						Unique: "next",
					},
				},
			},
		})
	})

	core.B.Handle(&nextBtn, func(c tele.Context) error {
		chatId := helpers.ParsePeer(c.Chat().ID)
		_, err := helpers.MovePlayList(chatId, "next")
		if err != nil {}

		return nil
	})

	core.B.Handle(&accioBtn, func(c tele.Context) error {
		respTime := time.Now()
		c.Bot().ChatByID(c.Chat().ID)
		latency := time.Since(respTime)
		text := fmt.Sprintf("Ping: %v\n", fmt.Sprintf("%dms", latency.Milliseconds()))

		upTime := time.Since(core.S)
		hours := int(upTime.Hours())
		minutes := int(upTime.Minutes()) % 60
		seconds := int(upTime.Seconds()) % 60

		var formattedDuration string
		if hours > 0 {
			formattedDuration = fmt.Sprintf("%dH:%02dM:%02dS", hours, minutes, seconds)
		} else {
			formattedDuration = fmt.Sprintf("%dM:%02dS", minutes, seconds)
		}

		text += fmt.Sprintf("Bot Uptime: %s\n", formattedDuration)

		mem := helpers.GetMemoryUsage()
		text += fmt.Sprintf("\nMemory Usage: %.2f%%\n", mem)
		nu, err := core.N.CpuUsage()
		if err == nil {
			text += fmt.Sprintf("Ntgcalls CPU: %.2f%%\n", nu)
		}

		return c.Respond(&tele.CallbackResponse{
			Text:      text,
			ShowAlert: true,
		})
	})
}
