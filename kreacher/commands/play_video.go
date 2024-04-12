package commands

import (
	"fmt"
	"strconv"
	"strings"

	tg "github.com/amarnathcjd/gogram/telegram"
	tele "gopkg.in/telebot.v3"
	hl "santiirepair.dev/kreacher/helpers"
	"santiirepair.dev/kreacher/ntgcalls"
	inst "santiirepair.dev/kreacher/instances"
)

func PlayVideo(c tele.Context) error {

	var err error
	var audioURL, videoURL string

	target := strings.Join(c.Args(), " ")
	if target != "" {
		switch hl.GetURLType(target) {
		case hl.YoutubeURL:
			audioURL, videoURL, err = hl.GetYoutubeStream(target)
			if err != nil {
				return err
			}
		case hl.CommonURL:
			audioURL = target
			videoURL = target
		case hl.NotURL:
			response, err := hl.YoutubeSearch(target)
			if err != nil {
				return nil
			}

			audioURL = response.AudioURL
			videoURL = response.VideoURL
		}

		x := strconv.FormatInt(c.Chat().ID, 10)
		y := strings.ReplaceAll(x, "-100", "")
		z, _ := strconv.ParseInt(y, 10, 64)

		channel, err := inst.U.GetChannel(z)
		if err != nil {
			return err
		}

		if calls := inst.N.Calls(); len(calls) > 0 {
			for chat := range calls {
				if chat == channel.ID {
					queue, err := hl.AddToQueue(c.Chat().ID, &hl.Queue{
						Requester:   c.Sender().ID,
						AudioSource: audioURL,
					})

					if err != nil {
						return err
					}

					return c.Reply(fmt.Sprintf("In queue %d", queue))
				}
			}
		}

		jsonParams, err := inst.N.CreateCall(channel.ID, ntgcalls.MediaDescription{
			Audio: &ntgcalls.AudioDescription{
				InputMode:     ntgcalls.InputModeShell,
				SampleRate:    96000,
				BitsPerSample: 16,
				ChannelCount:  2,
				Input:         fmt.Sprintf("ffmpeg -i %s -f s16le -ac 2 -ar 96k -v quiet pipe:1", audioURL),
			},
			Video: &ntgcalls.VideoDescription{
				InputMode: ntgcalls.InputModeShell,
				Width:     1920,
				Height:    1080,
				Fps:       60,
				Input:     fmt.Sprintf("ffmpeg -i %s -f rawvideo -r 60 -pix_fmt yuv420p -v quiet -vf scale=1920:1080 pipe:1", videoURL),
			},
		})

		if err != nil {
			return err
		}

		fullChatRaw, err := inst.U.ChannelsGetFullChannel(
			&tg.InputChannelObj{
				ChannelID:  channel.ID,
				AccessHash: channel.AccessHash,
			},
		)

		if err != nil {
			return err
		}

		fullChat := fullChatRaw.FullChat.(*tg.ChannelFull)

		me, err := inst.U.GetMe()
		if err != nil {
			return err
		}

		callResRaw, err := inst.U.PhoneJoinGroupCall(
			&tg.PhoneJoinGroupCallParams{
				Muted:        false,
				VideoStopped: false,
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

			_ = inst.N.Connect(channel.ID, updateTyped.Params.Data)
		}

		err = c.Send("Successful joined")

		return err

	}

	return err
}
