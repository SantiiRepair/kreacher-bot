package commands

import (
	"fmt"
	"strconv"
	"strings"

	tg "github.com/amarnathcjd/gogram/telegram"
	tele "gopkg.in/telebot.v3"
	h "santiirepair.dev/kreacher/helpers"
	"santiirepair.dev/kreacher/ntgcalls"
)

func PlayVideo(c tele.Context, u *tg.Client, n *ntgcalls.Client) error {
	var err error
	var target string

	target = strings.Join(c.Args(), " ")
	if target != "" {
		switch h.GetURLType(target) {
		case h.YOUTUBE_URL:
			target, _, err = h.GetYoutubeStream(target)
			if err != nil {
				return err
			}
		case h.ITS_NOT_A_URL:
			response, err := h.YoutubeSearch(target, h.Video)
			if err != nil {
				return nil
			}

			target = response.VideoURL
            fmt.Println(target)
		}

		x := strconv.FormatInt(c.Chat().ID, 10)
		y := strings.ReplaceAll(x, "-100", "")
		z, _ := strconv.ParseInt(y, 10, 64)

		channel, err := u.GetChannel(z)
		if err != nil {
			return err
		}

		if calls := n.Calls(); len(calls) > 0 {
			for chat := range calls {
				if chat == channel.ID {
					err = n.ChangeStream(chat, ntgcalls.MediaDescription{
						Video: &ntgcalls.VideoDescription{
							InputMode: ntgcalls.InputModeShell,
							Width:     1920,
							Height:    1080,
							Fps:       60,
							Input:     fmt.Sprintf("ffmpeg -i %s -f rawvideo -r 60 -pix_fmt yuv420p -v quiet -vf scale=1920:1080 pipe:1", target),
						},
					})

					return err
				}
			}
		}

		jsonParams, err := n.CreateCall(channel.ID, ntgcalls.MediaDescription{
			Video: &ntgcalls.VideoDescription{
				InputMode: ntgcalls.InputModeShell,
				Width:     1920,
				Height:    1080,
				Fps:       60,
				Input:     fmt.Sprintf("ffmpeg -i %s -f rawvideo -r 60 -pix_fmt yuv420p -v quiet -vf scale=1920:1080 pipe:1", target),
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

			_ = n.Connect(channel.ID, updateTyped.Params.Data)
		}

		err = c.Send("Successful joined")

		return err

	}

	return err
}
