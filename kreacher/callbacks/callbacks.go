package callbacks

import (
	"fmt"

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

	core.B.Handle(&pingBtn, func(c tele.Context) error {
		return c.Respond(&tele.CallbackResponse{
			ShowAlert: true,
			Text:      "Callback triggered!",
		})
	})
}
