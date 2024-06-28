package internal

import (
	"context"
	"math/rand"
	"time"

	"github.com/gotd/contrib/storage"
	"github.com/gotd/td/tg"
	"github.com/pkg/errors"
	"santiirepair.dev/kreacher/core"
	"santiirepair.dev/kreacher/logger"
)

func StartGroupCall(channel storage.Peer, params string, withVideo bool, muted bool) error {
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

	me, err := core.U.Self(context.Background())
	if err != nil {
		return err
	}

	call, ok := mcf.GetFullChat().GetCall()
	if !ok {
		logger.Warn("no calls for %d found, trying to create a new one", channel.Key.ID)

		rand.New(rand.NewSource(time.Now().UnixNano()))
		_, err := core.U.API().PhoneCreateGroupCall(context.Background(), &tg.PhoneCreateGroupCallRequest{
			RandomID: rand.Int(),
			Peer: &tg.InputPeerChannel{
				ChannelID:  channel.Key.ID,
				AccessHash: channel.Key.AccessHash,
			},
		})

		if err != nil {
			return err
		}

		mcf, err = core.U.API().ChannelsGetFullChannel(
			context.Background(),
			&tg.InputChannel{
				ChannelID:  channel.Key.ID,
				AccessHash: channel.Key.AccessHash,
			},
		)

		if err != nil {
			return err
		}

		call, ok = mcf.GetFullChat().GetCall()
		if !ok {
			return errors.Errorf("it was not possible to create the call for %d, check logger for details", channel.Key.ID)
		}

		logger.Info("created new call for %d", channel.Key.ID)
	}

	updates, err := core.U.API().PhoneJoinGroupCall(context.Background(), &tg.PhoneJoinGroupCallRequest{
		Muted:        muted,
		VideoStopped: !withVideo,
		Call:         call,
		Params: tg.DataJSON{
			Data: params,
		},
		JoinAs: &tg.InputPeerUser{
			UserID:     me.ID,
			AccessHash: me.AccessHash,
		},
	})

	if err != nil {
		return err
	}

	for _, update := range updates.(*tg.Updates).Updates {
		ut, ok := update.(*tg.UpdateGroupCallConnection)
		if !ok {
			continue
		}

		_ = core.N.Connect(channel.Key.ID, ut.Params.Data)
	}

	return nil
}
