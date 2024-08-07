package internal

import (
	"context"
	"math/rand"

	"github.com/gotd/contrib/storage"
	"github.com/gotd/td/tg"
	"github.com/pkg/errors"
	"santiirepair.dev/kreacher/core"
	"santiirepair.dev/kreacher/logger"
)

func GetPeer(peerId int64) (storage.Peer, error) {
	ctx := context.Background()
	channel, err := storage.FindPeer(ctx, core.PDB, &tg.PeerChannel{ChannelID: peerId})
	if err != nil {
		return storage.Peer{}, err
	}

	return channel, nil
}

func StartGroupCall(channel storage.Peer, params string, withVideo bool, muted bool) error {
	ctx := context.Background()
	mcf, err := core.U.API().ChannelsGetFullChannel(ctx, &tg.InputChannel{
		ChannelID:  channel.Key.ID,
		AccessHash: channel.Key.AccessHash,
	},
	)

	if err != nil {
		return err
	}

	me, err := core.U.Self(ctx)
	if err != nil {
		return err
	}

	call, ok := mcf.GetFullChat().GetCall()
	if !ok {
		logger.Warnf("no calls for %d found, trying to create a new one", channel.Key.ID)

		_, err := core.U.API().PhoneCreateGroupCall(ctx, &tg.PhoneCreateGroupCallRequest{
			RandomID: rand.Int(),
			Peer: &tg.InputPeerChannel{
				ChannelID:  channel.Key.ID,
				AccessHash: channel.Key.AccessHash,
			},
		})

		if err != nil {
			return err
		}

		mcf, err = core.U.API().ChannelsGetFullChannel(ctx, &tg.InputChannel{
			ChannelID:  channel.Key.ID,
			AccessHash: channel.Key.AccessHash,
		})

		if err != nil {
			return err
		}

		call, ok = mcf.GetFullChat().GetCall()
		if !ok {
			return errors.Errorf("it was not possible to create the call for %d, check logger for details", channel.Key.ID)
		}

		logger.Infof("created new call for %d", channel.Key.ID)
	}

	updates, err := core.U.API().PhoneJoinGroupCall(ctx, &tg.PhoneJoinGroupCallRequest{
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

		core.N.Connect(channel.Key.ID, ut.GetParams().Data)
	}

	return nil
}

func LeaveGroupCall(chatId int64) error {
	ctx := context.Background()
	channel, err := GetPeer(chatId)
	if err != nil {
		return err
	}

	mcf, err := core.U.API().ChannelsGetFullChannel(ctx, &tg.InputChannel{
		ChannelID:  channel.Key.ID,
		AccessHash: channel.Key.AccessHash,
	})

	if err != nil {
		return err
	}

	call, ok := mcf.GetFullChat().GetCall()
	if !ok {
		return errors.Errorf("it was not possible to leave the call for %d, check logger for details", channel.Key.ID)
	}

	_, err = core.U.API().PhoneLeaveGroupCall(ctx, &tg.PhoneLeaveGroupCallRequest{
		Call: tg.InputGroupCall{
			ID:         call.GetID(),
			AccessHash: call.GetAccessHash(),
		},
		Source: rand.Int(),
	})

	return err
}
