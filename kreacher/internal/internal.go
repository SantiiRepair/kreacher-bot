package internal

import (
	"context"
	"math/rand"
	"os"
	"os/exec"
	"strings"

	"github.com/gotd/contrib/storage"
	"github.com/gotd/td/tg"
	"github.com/pkg/errors"
	"santiirepair.dev/kreacher/core"
)

type GroupCallConfig tg.PhoneJoinGroupCallRequest

func GetPeer(peerId int64) (storage.Peer, error) {
	ctx := context.Background()
	channel, err := storage.FindPeer(ctx, core.PDB, &tg.PeerChannel{ChannelID: peerId})
	if err != nil {
		return storage.Peer{}, err
	}

	return channel, nil
}

func SetGroupCall(channel storage.Peer, params string, conf GroupCallConfig) error {
	ctx := context.Background()

	mcf, err := core.U.API().ChannelsGetFullChannel(ctx, &tg.InputChannel{
		ChannelID:  channel.Key.ID,
		AccessHash: channel.Key.AccessHash,
	})
	if err != nil {
		return err
	}

	me, err := core.U.Self(ctx)
	if err != nil {
		return err
	}

	call, ok := mcf.GetFullChat().GetCall()
	if !ok {
		if !channel.Channel.AdminRights.ManageCall {
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
				return errors.Errorf("I can't open the call on %d", channel.Key.ID)
			}
		} else {
			return errors.Errorf("I couldn't open the voice chat, am I an admin?")
		}
	}

	gc, err := core.U.API().PhoneGetGroupCall(ctx, &tg.PhoneGetGroupCallRequest{
		Call:  call,
		Limit: 1,
	})

	if err != nil {
		return err
	}

	joined := false
	for _, participant := range gc.Participants {
		if participant.Self {
			joined = true
			break
		}
	}

	var updates tg.UpdatesClass
	if !joined {
		updates, err = core.U.API().PhoneJoinGroupCall(ctx, &tg.PhoneJoinGroupCallRequest{
			Call:         call,
			Muted:        conf.Muted,
			VideoStopped: conf.VideoStopped,
			Params: tg.DataJSON{
				Data: params,
			},
			JoinAs: &tg.InputPeerUser{
				UserID:     me.ID,
				AccessHash: me.AccessHash,
			},
		})
	} else {
		updates, err = core.U.API().PhoneEditGroupCallParticipant(ctx, &tg.PhoneEditGroupCallParticipantRequest{
			Call:         call,
			Muted:        conf.Muted,
			VideoStopped: conf.VideoStopped,
			Participant:  me.AsInputPeer(),
		})
	}

	if err != nil {
		return err
	}

	for _, update := range updates.(*tg.Updates).Updates {
		if ut, ok := update.(*tg.UpdateGroupCallConnection); ok {
			core.N.Connect(channel.Key.ID, ut.GetParams().Data)
		}
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

func MediaConverter(input string, oc MediaType) (string, error) {
	//defer os.Remove(input)

	if _, err := os.Stat(input); os.IsNotExist(err) {
		return "", err
	}

	var cmd *exec.Cmd
	var outputFile string

	if oc == VIDEO {
		outputFile = strings.TrimSuffix(input, ".mp4") + ".mp4"
		cmd = exec.Command("ffmpeg", "-i", input, "-c:v", "copy", "-c:a", "aac", outputFile)
	} else if oc == AUDIO {
		outputFile = strings.TrimSuffix(input, ".mp3") + ".mp3"
		cmd = exec.Command("ffmpeg", "-i", input, outputFile)
	} else {
		return "", nil
	}

	err := cmd.Run()
	if err != nil {
		return "", err
	}

	return outputFile, nil
}
