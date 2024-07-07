package commands

import (
	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/core"
	"santiirepair.dev/kreacher/helpers"
	"santiirepair.dev/kreacher/internal"
)

func leave(c tele.Context) error {
	peerId := helpers.ParsePeer(c.Chat().ID)
	if calls := core.N.Calls(); len(calls) > 0 {
		for chat := range calls {
			if chat == peerId {
				err := core.N.Stop(chat)
				if err != nil {
					return err
				}

				err = helpers.DeleteQueue(chat)
				if err != nil {
					return err
				}

				err = internal.LeaveGroupCall(chat)
				if err != nil {
					return err
				}

				return c.Reply("Stream cut off, queues emptied")
			}
		}
	}

	return c.Reply("No active streams were found in this chat")
}
