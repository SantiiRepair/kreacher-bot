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

func PlaySong(c tele.Context, u *tg.Client, n *ntgcalls.Client) error {
	if c.Chat().Type == tele.ChatPrivate {
		return c.Send("*_This command is only for groups or channels_*", tele.ParseMode(tele.ModeMarkdownV2))
	}

	var err error
	var link string

	target := strings.Join(c.Args(), " ")
	if target != "" {
		switch h.GetURLType(target) {
		case h.YOUTUBE_URL:
			link, _, err = h.GetYoutubeStream(target)
			if err != nil {
				return err
			}
		case h.COMMON_URL:
			link = target
		case h.ITS_NOT_A_URL:
			response, err := h.YtSearch(target)
			if err != nil {
				return nil
			}

			link = response.URL
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
						Audio: &ntgcalls.AudioDescription{
							InputMode:     ntgcalls.InputModeShell,
							SampleRate:    96000,
							BitsPerSample: 16,
							ChannelCount:  2,
							Input:         fmt.Sprintf("ffmpeg -i %s -f s16le -ac 2 -ar 96k -v quiet pipe:1", link),
						},
					})

					return err
				}
			}
		}

		jsonParams, err := n.CreateCall(channel.ID, ntgcalls.MediaDescription{
			Audio: &ntgcalls.AudioDescription{
				InputMode:     ntgcalls.InputModeShell,
				SampleRate:    96000,
				BitsPerSample: 16,
				ChannelCount:  2,
				Input:         fmt.Sprintf("ffmpeg -i %s -f s16le -ac 2 -ar 96k -v quiet pipe:1", link),
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

		err = c.Send("Successful joined")

		return err

	}

	return err
}
