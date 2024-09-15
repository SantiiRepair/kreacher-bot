package commands

import (
	"context"
	"fmt"
	"strconv"
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

		message, err := c.Bot().Send(c.Recipient(), helpers.EscapeMarkdownV2("*Fetching data...*"))
		if err != nil {
			return err
		}
		defer c.Bot().Delete(&tele.StoredMessage{ChatID: message.Chat.ID, MessageID: strconv.Itoa(message.ID)})

		videoPath, err := helpers.Download(mediaInfo, "bestvideo+bestaudio/best")
		if err != nil {
			return err
		}

		c.Bot().Edit(tele.StoredMessage{ChatID: message.Chat.ID, MessageID: strconv.Itoa(message.ID)}, helpers.EscapeMarkdownV2("*Buffering media content...*"))

		audioPath, err := internal.MediaConverter(videoPath, internal.AUDIO)
		if err != nil {
			return err
		}

		mediaDescription := ntgcalls.MediaDescription{
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
		}

		if calls := core.N.Calls(); len(calls) > 0 {
			for chat := range calls {
				if chat == channel.Key.ID {
					if err = core.N.ChangeStream(channel.Key.ID, mediaDescription); err != nil {
						return err
					}
					break
				}
			}
		} else {
			params, err := core.N.CreateCall(channel.Key.ID, mediaDescription)
			if err != nil {
				return err
			}

			if err = internal.SetGroupCall(channel, params, internal.GroupCallConfig{Muted: false, VideoStopped: false}); err != nil {
				return c.Send(fmt.Sprintf("*%v*", err))
			}
		}

		caption := fmt.Sprintf("*Broadcasting* \n\n *Title: %s*", mediaInfo.Title)
		return c.Send(helpers.EscapeMarkdownV2(caption), &tele.ReplyMarkup{
			InlineKeyboard: [][]tele.InlineButton{
				{
					{Text: "⏮", Data: "", Unique: "prev"},
					{Text: "⏸️", Data: "", Unique: "pause"},
					{Text: "⏭️", Data: "", Unique: "next"},
				},
			},
		})

	}

	return nil
}
