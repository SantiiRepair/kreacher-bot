package main

//#cgo LDFLAGS: -L . -lntgcalls -Wl,-rpath=./
import "C"
import (
	"fmt"
	"os"
	"os/signal"
	"sync"
	"syscall"

	tele "gopkg.in/telebot.v3"
	"santiirepair.dev/kreacher/commands"
	inst "santiirepair.dev/kreacher/instances"
	"santiirepair.dev/kreacher/ntgcalls"
)

func main() {

	var wg sync.WaitGroup

	if err := inst.B.SetCommands([]tele.Command{
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

	inst.N.OnStreamEnd(func(chatId int64, streamType ntgcalls.StreamType) {
		fmt.Println(chatId)
	})

	inst.N.OnConnectionChange(func(chatId int64, state ntgcalls.ConnectionState) {
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
		inst.B.Start()
	}()

	wg.Add(1)
	go func() {
		defer wg.Done()
		inst.U.Idle()
	}()

	go commands.Start()

	inst.CY.Printf("\n\nBot @%s started, receiving updates...\n", inst.B.Me.Username)

	wg.Wait()

}
