package commands

// const re = "^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"

import (
	"fmt"
	"regexp"
	"strings"

	tg "github.com/amarnathcjd/gogram/telegram"
	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/helpers"
	"santiirepair.dev/kreacher/ntgcalls"
)

func PlaySong(c tele.Context, u *tg.Client, n *ntgcalls.Client) error {
	var err error
	var link string

	target := strings.Join(c.Args(), " ")
	if target != "" {
		re := regexp.MustCompile(`^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+`)
		if re.MatchString(target) {
			link, _, err = helpers.GetYoutubeStream(target)

			if err != nil {
				return err
			}
		} else {
			link = target
		}

		jsonParams, err := n.CreateCall(c.Chat().ID, ntgcalls.MediaDescription{
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

		rawObj, _ := u.ResolveUsername(c.Chat().Username)

		channel := rawObj.(*tg.Channel)

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
			switch update.(type) {
			case *tg.UpdateGroupCallConnection:
				phoneCall := update.(*tg.UpdateGroupCallConnection)
				_ = n.Connect(channel.ID, phoneCall.Params.Data)
			}
		}

		err = c.Send("Successful joined")

		return err

	}

	return err
}
