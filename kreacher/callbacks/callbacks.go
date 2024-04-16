package callbacks

import (
	"fmt"
	"math"
	"time"

	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/core"
	"santiirepair.dev/kreacher/helpers"
	"santiirepair.dev/kreacher/ntgcalls"
)

func Start() {
	core.B.Handle(&prevBtn, func(c tele.Context) error {
		chatId := helpers.ParsePeer(c.Chat().ID)
		result, err := helpers.MovePlayList(chatId, "prev")
		if err != nil {
			return err
		}

		if result != nil {
			var desc ntgcalls.MediaDescription
			desc.Audio = &ntgcalls.AudioDescription{
				InputMode:     ntgcalls.InputModeShell,
				SampleRate:    96000,
				BitsPerSample: 16,
				ChannelCount:  2,
				Input:         fmt.Sprintf("ffmpeg -i %s -f s16le -ac 2 -ar 96k -v quiet pipe:1", result.AudioSource),
			}
			if result.VideoSource != "" {
				desc.Video = &ntgcalls.VideoDescription{
					InputMode: ntgcalls.InputModeShell,
					Width:     1920,
					Height:    1080,
					Fps:       60,
					Input:     fmt.Sprintf("ffmpeg -i %s -f rawvideo -r 60 -pix_fmt yuv420p -v quiet -vf scale=1920:1080 pipe:1", result.VideoSource),
				}
			}

			err = core.N.ChangeStream(chatId, desc)
			if err != nil {
				return err
			}

			return c.Respond(&tele.CallbackResponse{
				Text: "Callback triggered!",
			})
		}

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
		result, err := helpers.MovePlayList(chatId, "next")
		if err != nil {
			return err
		}

		if result != nil {
			var desc ntgcalls.MediaDescription
			desc.Audio = &ntgcalls.AudioDescription{
				InputMode:     ntgcalls.InputModeShell,
				SampleRate:    96000,
				BitsPerSample: 16,
				ChannelCount:  2,
				Input:         fmt.Sprintf("ffmpeg -i %s -f s16le -ac 2 -ar 96k -v quiet pipe:1", result.AudioSource),
			}

			if result.VideoSource != "" {
				desc.Video = &ntgcalls.VideoDescription{
					InputMode: ntgcalls.InputModeShell,
					Width:     1920,
					Height:    1080,
					Fps:       60,
					Input:     fmt.Sprintf("ffmpeg -i %s -f rawvideo -r 60 -pix_fmt yuv420p -v quiet -vf scale=1920:1080 pipe:1", result.VideoSource),
				}
			}

			err = core.N.ChangeStream(chatId, desc)
			if err != nil {
				return err
			}

			return c.Respond()
		}

		return nil
	})

	core.B.Handle(&accioBtn, func(c tele.Context) error {
		respTime := time.Now()
		c.Bot().ChatByID(c.Chat().ID)
		latency := time.Since(respTime)
		text := fmt.Sprintf("Ping: %v\n", fmt.Sprintf("%dms", latency.Milliseconds()))

		upTime := time.Since(core.S)
		hours := math.Round(upTime.Hours())
		minutes := math.Round(upTime.Minutes())
		seconds := math.Round(upTime.Seconds())

		var formattedDuration string

		if hours > 0 {
			formattedDuration = fmt.Sprintf("%.0f hours", hours)
		} else if minutes > 0 {
			formattedDuration = fmt.Sprintf("%.0f minutes", minutes)
		} else {
			formattedDuration = fmt.Sprintf("%.0f seconds", seconds)
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
