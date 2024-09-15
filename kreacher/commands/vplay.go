package commands

import (
	"context"
	"fmt"
	"strings"

	"github.com/gotd/contrib/storage"
	"github.com/gotd/td/tg"
	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/core"
	"santiirepair.dev/kreacher/helpers"
	"santiirepair.dev/kreacher/internal"
	"santiirepair.dev/kreacher/ntgcalls"
)

func vplay(c tele.Context) error {
	target := strings.Join(c.Args(), " ")
	if target != "" {
		peerId := helpers.ParsePeer(c.Chat().ID)
		channel, err := storage.FindPeer(context.Background(), core.PDB, &tg.PeerChannel{ChannelID: peerId})
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

		videoPath, err := helpers.Download(mediaInfo, "bestvideo+bestaudio/best")
		if err != nil {
			return err
		}

		audioPath, err := internal.MediaConverter(videoPath, internal.AUDIO)
		if err != nil {
			return err
		}

		params, err := core.N.CreateCall(channel.Key.ID, ntgcalls.MediaDescription{
			Audio: &ntgcalls.AudioDescription{
				ChannelCount:  2,
				BitsPerSample: 16,
				SampleRate:    96000,
				InputMode:     ntgcalls.InputModeShell,
				Input:         fmt.Sprintf("sox %s -t wav -r 96k -c 2 -b 16 - gain 8", audioPath),
			},
			Video: &ntgcalls.VideoDescription{
				Fps:       30,
				Width:     1920,
				Height:    1080,
				InputMode: ntgcalls.InputModeShell,
				Input:     fmt.Sprintf("ffmpeg -i %s -f rawvideo -r 30 -pix_fmt yuv420p -v quiet -vf scale=1920:1080 -b:v 5000k -preset fast -bufsize 10000k pipe:1", videoPath),
			},
		})

		if err != nil {
			return err
		}

		err = internal.SetGroupCall(channel, params, true, false)
		if err != nil {
			return err
		}

		return c.Send("Successful joined", &tele.ReplyMarkup{
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

	}

	return nil
}
