package commands

import (
	"fmt"
	"strings"

	tg "github.com/amarnathcjd/gogram/telegram"
	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/core"
	"santiirepair.dev/kreacher/helpers"
	"santiirepair.dev/kreacher/ntgcalls"
)

func playVideo(c tele.Context) error {

	var err error
	var audioURL, videoURL string

	target := strings.Join(c.Args(), " ")
	if target != "" {
		switch helpers.GetURLType(target) {
		case helpers.YoutubeURL:
			audioURL, videoURL, err = helpers.GetYoutubeStream(target)
			if err != nil {
				return err
			}
		case helpers.CommonURL:
			audioURL = target
			videoURL = target
		case helpers.NotURL:
			response, err := helpers.YoutubeSearch(target)
			if err != nil {
				return nil
			}

			audioURL = response.AudioURL
			videoURL = response.VideoURL
		}

		peerId := helpers.ParsePeer(c.Chat().ID)

		channel, err := core.U.GetChannel(peerId)
		if err != nil {
			return err
		}

		queue, err := helpers.AddToPlayList(peerId, &helpers.Queue{
			Requester:   c.Sender().ID,
			AudioSource: audioURL,
			VideoSource: videoURL,
		})

		if err != nil {
			return err
		}

		if calls := core.N.Calls(); len(calls) > 0 {
			for chat := range calls {
				if chat == channel.ID {
					return c.Reply(fmt.Sprintf("In queue %d", queue))
				}
			}
		}

		jsonParams, err := core.N.CreateCall(channel.ID, ntgcalls.MediaDescription{
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

		fullChatRaw, err := core.U.ChannelsGetFullChannel(
			&tg.InputChannelObj{
				ChannelID:  channel.ID,
				AccessHash: channel.AccessHash,
			},
		)

		if err != nil {
			return err
		}

		fullChat := fullChatRaw.FullChat.(*tg.ChannelFull)

		me, err := core.U.GetMe()
		if err != nil {
			return err
		}

		callResRaw, err := core.U.PhoneJoinGroupCall(
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

			_ = core.N.Connect(channel.ID, updateTyped.Params.Data)
		}

		err = c.Send("Successful joined", &tele.ReplyMarkup{
			InlineKeyboard: [][]tele.InlineButton{
				{
					{
						Text:   "Prev",
						Data:   "",
						Unique: "prev",
					},
					{
						Text:   "Pause",
						Data:   "",
						Unique: "pause",
					},
					{
						Text:   "Next",
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
