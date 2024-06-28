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
	"santiirepair.dev/kreacher/ntgcalls"
)

func play(c tele.Context) error {

	var err error
	var audioURL string

	target := strings.Join(c.Args(), " ")
	if target == "" {
		return c.Reply(forgottenUsage, tele.ParseMode(tele.ModeMarkdownV2), tele.NoPreview)
	}

	switch helpers.GetURLType(target) {
	case helpers.YoutubeURL:
		audioURL, _, err = helpers.GetYoutubeStream(target)
		if err != nil {
			return err
		}

	case helpers.CommonURL:
		audioURL = target
	case helpers.NotURL:
		response, err := helpers.YoutubeSearch(target)

		if err != nil {
			return nil
		}

		audioURL = response.AudioURL
	}

	peerId := helpers.ParsePeer(c.Chat().ID)

	channel, err := storage.FindPeer(context.Background(), core.PDB, &tg.PeerChannel{ChannelID: c.Chat().ID})
	if err != nil {
		return err
	}

	queue, err := helpers.AddToPlayList(peerId, &helpers.Queue{
		Requester:   c.Sender().ID,
		AudioSource: audioURL,
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

	jsonParams, err := core.N.CreateCall(channel.Key.ID, ntgcalls.MediaDescription{
		Audio: &ntgcalls.AudioDescription{
			InputMode:     ntgcalls.InputModeShell,
			SampleRate:    96000,
			BitsPerSample: 16,
			ChannelCount:  2,
			Input:         fmt.Sprintf("ffmpeg -i %s -f s16le -ac 2 -ar 96k -v quiet pipe:1", audioURL),
		},
	})

	if err != nil {
		return err
	}

	mcf, err := core.U.API().ChannelsGetFullChannel(
		context.Background(),
		&tg.InputChannel{
			ChannelID:  channel.Key.ID,
			AccessHash: channel.Key.AccessHash,
		},
	)

	if err != nil {
		return err
	}

	fullChat := mcf.FullChat.(*tg.ChannelFull)

	me, err := core.U.Self(context.Background())
	if err != nil {
		return err
	}

	_, err = core.U.API().PhoneJoinGroupCall(
		context.Background(),
		&tg.PhoneJoinGroupCallRequest{
			Muted:        false,
			VideoStopped: true,
			Call:         fullChat.Call,
			Params: tg.DataJSON{
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

	/*callRes := updates
	for _, update := range callRes.Updates {
		updateTyped, ok := update.(*tg.UpdateGroupCallConnection)
		if !ok {
			continue
		}

		_ = core.N.Connect(channel.Key.ID, jsonParams)
	}*/

	_ = core.N.Connect(channel.Key.ID, jsonParams)

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

var forgottenUsage = `
It seems you forgot something 🤔\!

If you have any questions or problems with the command we recommend reading our [wiki](https://github.com/SantiiRepair/kreacher-bot/wiki/Usage#play)
`
