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

	var err error
	var mediaInfo helpers.MediaInfo

	target := strings.Join(c.Args(), " ")
	if target != "" {
		peerId := helpers.ParsePeer(c.Chat().ID)
		channel, err := storage.FindPeer(context.Background(), core.PDB, &tg.PeerChannel{ChannelID: peerId})
		if err != nil {
			return err
		}

		queue, err := helpers.AddToPlayList(peerId, &helpers.Queue{
			Command:     PLAY_VIDEO,
			Requester:   c.Sender().ID,
			OriginalUrl: mediaInfo.OriginalUrl,
		})

		if err != nil {
			return err
		}

		if calls := core.N.Calls(); len(calls) > 0 {
			for chat := range calls {
				if chat == channel.Key.ID {
					return c.Reply(fmt.Sprintf("In queue %d", queue))
				}
			}
		}

		params, err := core.N.CreateCall(channel.Key.ID, ntgcalls.MediaDescription{
			Audio: &ntgcalls.AudioDescription{
				ChannelCount:  2,
				BitsPerSample: 16,
				SampleRate:    96000,
				InputMode:     ntgcalls.InputModeShell,
				Input:         fmt.Sprintf("ffmpeg -i %s -f s16le -ac 2 -ar 96k -v quiet pipe:1", mediaInfo.URL),
			},
			Video: &ntgcalls.VideoDescription{
				Fps:       60,
				Width:     1920,
				Height:    1080,
				InputMode: ntgcalls.InputModeShell,
				Input:     fmt.Sprintf("ffmpeg -i %s -f rawvideo -r 60 -pix_fmt yuv420p -v quiet -vf scale=1920:1080 pipe:1", mediaInfo.URL),
			},
		})

		if err != nil {
			return err
		}

		err = internal.StartGroupCall(channel, params, true, false)
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

	return err
}
