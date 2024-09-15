package helpers

import (
	"fmt"

	"net/http"
	"net/url"
	"reflect"
	"strconv"
	"strings"
)

type SourceType int

const (
	YoutubeURL SourceType = iota
	CommonURL
	NotURL
)

func ParsePeer(chatId int64) int64 {
	x := strconv.FormatInt(chatId, 10)
	y := strings.ReplaceAll(x, "-100", "")
	z, _ := strconv.ParseInt(y, 10, 64)

	return z
}

func UnparsePeer(peerId int64) int64 {
	x := strconv.FormatInt(peerId, 10)
	y := fmt.Sprintf("-100%s", x)
	z, _ := strconv.ParseInt(y, 10, 64)

	return z
}

func UrlExists(url string) bool {
	resp, err := http.Get(url)
	if err != nil {
		return false
	}

	defer resp.Body.Close()

	return resp.StatusCode == http.StatusOK
}

func isURL(s string) bool {
	u, err := url.Parse(s)
	if err != nil || u.Scheme == "" || u.Host == "" {
		return false
	}

	return true
}

func reverseSlice(s interface{}) interface{} {
	val := reflect.ValueOf(s)
	if val.Kind() != reflect.Slice {
		return nil
	}

	reversed := reflect.MakeSlice(val.Type(), val.Len(), val.Cap())
	for i := 0; i < val.Len(); i++ {
		reversed.Index(i).Set(val.Index(val.Len() - 1 - i))
	}

	return reversed.Interface()
}

func EscapeMarkdownV2(text string) string {
	specialChars := []string{"_", "[", "]", "-", "(", ")", "~", ">", "#", "+", "=", "|", "{", "}", ".", "!"}
	for _, char := range specialChars {
		text = strings.ReplaceAll(text, char, "\\"+char)
	}

	return text
}
