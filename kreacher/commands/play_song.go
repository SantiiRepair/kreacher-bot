package commands

import (
	"fmt"
	"strconv"
	"strings"

	tg "github.com/amarnathcjd/gogram/telegram"
	"github.com/redis/go-redis/v9"
	tele "gopkg.in/telebot.v3"
	hl "santiirepair.dev/kreacher/helpers"
	"santiirepair.dev/kreacher/ntgcalls"
)

func PlaySong(c tele.Context, r *redis.Client, u *tg.Client, n *ntgcalls.Client) error {

	var err error
	var audioURL string

	target := strings.Join(c.Args(), " ")
	if target != "" {
		switch hl.GetURLType(target) {
		case hl.YOUTUBE_URL:
			audioURL, _, err = hl.GetYoutubeStream(target)
			if err != nil {
				return err
			}

		case hl.COMMON_URL:
			audioURL = target
		case hl.ITS_NOT_A_URL:
			response, err := hl.YoutubeSearch(target, hl.Audio)
			if err != nil {
				return nil
			}

			audioURL = response.AudioURL
		}

		x := strconv.FormatInt(c.Chat().ID, 10)
		y := strings.ReplaceAll(x, "-100", "")
		z, _ := strconv.ParseInt(y, 10, 64)

		channel, err := u.GetChannel(z)
		if err != nil {
			return err
		}

		inputAudio := fmt.Sprintf("ffmpeg -i %s -f s16le -ac 2 -ar 96k -v quiet pipe:1", audioURL)

		if calls := n.Calls(); len(calls) > 0 {
			for chat := range calls {
				if chat == channel.ID {
					queueNumber, err := hl.AddToQueue(r, c.Chat().ID, &hl.Queue{
						Requester:   c.Sender().ID,
						AudioStream: audioURL,
					})

					if err != nil {
						return err
					}

					return c.Reply(fmt.Sprintf("In queue %d", queueNumber))
				}
			}
		}

		jsonParams, err := n.CreateCall(channel.ID, ntgcalls.MediaDescription{
			Audio: &ntgcalls.AudioDescription{
				InputMode:     ntgcalls.InputModeShell,
				SampleRate:    96000,
				BitsPerSample: 16,
				ChannelCount:  2,
				Input:         inputAudio,
			},
		})

		if err != nil {
			return err
		}

		fullChatRaw, err := u.ChannelsGetFullChannel(
			&tg.InputChannelObj{
				ChannelID:  channel.ID,
				AccessHash: channel.AccessHash,
			},
		)

		if err != nil {
			return err
		}

		fullChat := fullChatRaw.FullChat.(*tg.ChannelFull)

		me, err := u.GetMe()
		if err != nil {
			return err
		}

		callResRaw, err := u.PhoneJoinGroupCall(
			&tg.PhoneJoinGroupCallParams{
				Muted:        false,
				VideoStopped: true,
				Call:         fullChat.Call,
				Params: &tg.DataJson{
					Data: jsonParams,
				},
				JoinAs: &tg.InputPeerUser{
					UserID:     me.ID,
					AccessHash: me.AccessHash,
				},
			},
		)

		if err != nil {
			return err
		}

		callRes := callResRaw.(*tg.UpdatesObj)
		for _, update := range callRes.Updates {
			updateTyped, ok := update.(*tg.UpdateGroupCallConnection)
			if !ok {
				continue
			}

			_ = n.Connect(channel.ID, updateTyped.Params.Data)
		}

		err = c.Reply("Successful joined")

		return err

	}

	return err
}
