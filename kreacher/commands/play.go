package commands

import (
	"fmt"
	"strings"

	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/core"
	"santiirepair.dev/kreacher/helpers"
	"santiirepair.dev/kreacher/internal"
	"santiirepair.dev/kreacher/ntgcalls"
)

func play(c tele.Context) error {
	target := strings.Join(c.Args(), " ")
	if target == "" {
		return c.Reply(forgottenUsage, tele.ParseMode(tele.ModeMarkdownV2), tele.NoPreview)
	}

	peerId := helpers.ParsePeer(c.Chat().ID)
	channel, err := internal.GetPeer(peerId)
	if err != nil {
		return err
	}

	var mediaInfo helpers.MediaInfo
	err = helpers.GetMediaInfo(target, &mediaInfo)
	if err != nil {
		return err
	}

	if calls := core.N.Calls(); len(calls) > 0 {
		for chat := range calls {
			if chat == channel.Key.ID {
				queue, err := helpers.AddToPlayList(peerId, &helpers.Queue{
					Command:     PLAY_VIDEO,
					Requester:   c.Sender().ID,
					OriginalUrl: mediaInfo.OriginalUrl,
				})

				if err != nil {
					return err
				}

				return c.Reply(fmt.Sprintf("In queue %d", queue))
			}
		}
	}

	filepath, err := helpers.Download(mediaInfo, "bestaudio/best")
	if err != nil {
		return err
	}

	filepath, err = internal.AutoConvert(filepath)
	if err != nil {
		return err
	}

	params, err := core.N.CreateCall(channel.Key.ID, ntgcalls.MediaDescription{
		Audio: &ntgcalls.AudioDescription{
			ChannelCount:  2,
			BitsPerSample: 16,
			SampleRate:    96000,
			InputMode:     ntgcalls.InputModeShell,
			Input:         fmt.Sprintf("sox %s -t wav -r 96k -c 2 -b 16 - gain 8", filepath),
		},
	})

	if err != nil {
		return err
	}

	err = internal.StartGroupCall(channel, params, false, false)
	if err != nil {
		return err
	}

	err = c.Send("Successful joined", &tele.ReplyMarkup{
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

	return err
}
