package commands

import (
	"fmt"
	"strconv"
	"strings"

	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/core"
	"santiirepair.dev/kreacher/helpers"
	"santiirepair.dev/kreacher/internal"
	"santiirepair.dev/kreacher/ntgcalls"
)

func play(c tele.Context) error {
	target := strings.Join(c.Args(), " ")
	if target == "" {
		return c.Reply(forgottenUsage, tele.ParseMode(tele.ModeMarkdownV2), tele.NoPreview)
	}

	peerId := helpers.ParsePeer(c.Chat().ID)
	channel, err := internal.GetPeer(peerId)
	if err != nil {
		return err
	}

	var mediaInfo helpers.MediaInfo
	if err = helpers.GetMediaInfo(target, &mediaInfo); err != nil {
		return err
	}

	message, err := c.Bot().Send(c.Recipient(), helpers.EscapeMarkdownV2("*Fetching data...*"))
	if err != nil {
		return err
	}
	defer c.Bot().Delete(&tele.StoredMessage{ChatID: message.Chat.ID, MessageID: strconv.Itoa(message.ID)})

	filePath, err := helpers.Download(mediaInfo, "bestaudio/best")
	if err != nil {
		return err
	}

	c.Bot().Edit(tele.StoredMessage{ChatID: message.Chat.ID, MessageID: strconv.Itoa(message.ID)}, helpers.EscapeMarkdownV2("*Buffering media content...*"))

	audioPath, err := internal.MediaConverter(filePath, internal.AUDIO)
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

		if err = internal.SetGroupCall(channel, params, false, false); err != nil {
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
