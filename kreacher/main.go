package main

//#cgo LDFLAGS: -L . -lntgcalls -Wl,-rpath=./
import "C"
import (
	"fmt"
	"os"
	"os/exec"
	"os/signal"
	"sync"
	"syscall"

	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/commands"
	"santiirepair.dev/kreacher/core"
	"santiirepair.dev/kreacher/helpers"
	"santiirepair.dev/kreacher/logger"
	"santiirepair.dev/kreacher/ntgcalls"
)

func init() {
	_, err := exec.LookPath("yt-dlp")
	if err != nil {
		panic("yt-dlp isn't installed")
	}

	_, err = exec.LookPath("speedtest")
	if err != nil {
		panic("speedtest isn't installed")
	}
}

func main() {

	var wg sync.WaitGroup

	if err := core.B.SetCommands([]tele.Command{
		{Text: "config", Description: "Set the bot's configuration"},
		{Text: "help", Description: "How to use this"},
		{Text: "ping", Description: "Check the server's latency"},
		{Text: "play_book", Description: "Play a pdf or epub file as an audio book"},
		{Text: "play_song", Description: "Play audio in the voice chat"},
		{Text: "play_video", Description: "Play video in the voice chat"},
		{Text: "streaming", Description: "Any movie or series"},
	}); err != nil {
		panic(err)
	}

	core.N.OnStreamEnd(func(chatId int64, streamType ntgcalls.StreamType) {
		result, err := helpers.ChangeQueue(chatId, "next")
		if err != nil {
			logger.Error(err)
			return
		}

		var desc ntgcalls.MediaDescription
		desc.Audio = &ntgcalls.AudioDescription{
			InputMode:     ntgcalls.InputModeShell,
			SampleRate:    96000,
			BitsPerSample: 16,
			ChannelCount:  2,
			Input:         fmt.Sprintf("ffmpeg -i %s -f s16le -ac 2 -ar 96k -v quiet pipe:1", result.AudioSource),
		}
		if result.VideoSource != "" {
			desc.Video = &ntgcalls.VideoDescription{
				InputMode: ntgcalls.InputModeShell,
				Width:     1920,
				Height:    1080,
				Fps:       60,
				Input:     fmt.Sprintf("ffmpeg -i %s -f rawvideo -r 60 -pix_fmt yuv420p -v quiet -vf scale=1920:1080 pipe:1", result.VideoSource),
			}
		}

		err = core.N.ChangeStream(chatId, desc)
		if err != nil {
			logger.Error(err)
		}
	})

	core.N.OnConnectionChange(func(chatId int64, state ntgcalls.ConnectionState) {
		switch state {
		case ntgcalls.Connecting:
			fmt.Println("Connecting with chatId:", chatId)
		case ntgcalls.Connected:
			fmt.Println("Connected with chatId:", chatId)
		case ntgcalls.Failed:
			fmt.Println("Failed with chatId:", chatId)
		case ntgcalls.Timeout:
			fmt.Println("Timeout with chatId:", chatId)
		case ntgcalls.Closed:
			fmt.Println("Closed with chatId:", chatId)
		}
	})

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT)

	go func() {
		<-sigChan
		fmt.Println("\nReceived SIGINT, exiting...")

		wg.Done()
	}()

	wg.Add(1)
	go func() {
		defer wg.Done()
		core.B.Start()
	}()

	wg.Add(1)
	go func() {
		defer wg.Done()
		core.U.Idle()
	}()

	go commands.Start()

	core.CY.Printf("\n\nBot @%s started, receiving updates...\n", core.B.Me.Username)

	wg.Wait()

}
