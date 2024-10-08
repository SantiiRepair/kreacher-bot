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
	"santiirepair.dev/kreacher/callbacks"
	"santiirepair.dev/kreacher/commands"
	"santiirepair.dev/kreacher/core"
	"santiirepair.dev/kreacher/logger"
	"santiirepair.dev/kreacher/ntgcalls"
)

func init() {
	tools := []string{"yt-dlp", "ffmpeg", "sox", "speedtest"}
	for _, tool := range tools {
		_, err := exec.LookPath(tool)
		if err != nil {
			fmt.Printf("%s is not installed\n", tool)
			os.Exit(1)
		}
	}
}

func main() {

	var wg sync.WaitGroup

	if err := core.B.SetCommands([]tele.Command{
		{Text: "config", Description: "Set the bot's configuration"},
		{Text: "accio", Description: "Check the server's latency"},
		{Text: "play", Description: "Play audio in the voice chat"},
		{Text: "vplay", Description: "Play video in the voice chat"},
		{Text: "bplay", Description: "Play a pdf or epub file as an audio book"},
		{Text: "streaming", Description: "Any movie or series"},
		{Text: "help", Description: "How to use this"},
	}); err != nil {
		panic(err)
	}

	core.N.OnStreamEnd(func(chatId int64, streamType ntgcalls.StreamType) {})

	core.N.OnConnectionChange(func(chatId int64, state ntgcalls.ConnectionState) {
		switch state {
		case ntgcalls.Connecting:
			logger.Infof("connecting with chatId: %d", chatId)
		case ntgcalls.Connected:
			logger.Infof("connected with chatId: %d", chatId)
		case ntgcalls.Failed:
			logger.Infof("failed with chatId: %d", chatId)
		case ntgcalls.Timeout:
			logger.Infof("timeout with chatId: %d", chatId)
		case ntgcalls.Closed:
			logger.Infof("closed with chatId: %d", chatId)
		}
	})

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT)

	go func() {
		<-sigChan
		fmt.Println("\nReceived SIGINT, exiting...")
		core.B.Close()
		wg.Done()
	}()

	wg.Add(1)
	go func() {
		defer wg.Done()
		core.B.Start()
	}()

	go commands.Start()
	go callbacks.Start()

	fmt.Println("\nListening for updates. Interrupt (Ctrl+C) to stop.")

	wg.Wait()

}
