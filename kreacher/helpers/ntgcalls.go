package helpers

import (
	tg "github.com/amarnathcjd/gogram/telegram"
	"santiirepair.dev/kreacher/ntgcalls"
)

func JoinGroupCall(client *ntgcalls.Client, mtproto *tg.Client, username string) {
	me, _ := mtproto.GetMe()
	rawChannel, _ := mtproto.ResolveUsername(username)
	channel := rawChannel.(*tg.Channel)
	jsonParams, _ := client.CreateCall(channel.ID, ntgcalls.MediaDescription{
		Audio: &ntgcalls.AudioDescription{
			InputMode:     ntgcalls.InputModeShell,
			SampleRate:    96000,
			BitsPerSample: 16,
			ChannelCount:  2,
			Input:         "ffmpeg -i https://docs.evostream.com/sample_content/assets/sintel1m720p.mp4 -f s16le -ac 2 -ar 96k -v quiet pipe:1",
		},
	})
	fullChatRaw, _ := mtproto.ChannelsGetFullChannel(
		&tg.InputChannelObj{
			ChannelID:  channel.ID,
			AccessHash: channel.AccessHash,
		},
	)
	fullChat := fullChatRaw.FullChat.(*tg.ChannelFull)
	callResRaw, _ := mtproto.PhoneJoinGroupCall(
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
	callRes := callResRaw.(*tg.UpdatesObj)
	for _, update := range callRes.Updates {
		switch update.(type) {
		case *tg.UpdateGroupCallConnection:
			phoneCall := update.(*tg.UpdateGroupCallConnection)
			_ = client.Connect(channel.ID, phoneCall.Params.Data)
		}
	}
}
