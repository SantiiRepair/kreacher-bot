package helpers

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	"errors"

	"github.com/google/uuid"
)

type MediaInfo struct {
	Title       string   `json:"title"`
	Filename    string   `json:"filename"`
	Duration    float64  `json:"duration"`
	Thumbnail   string   `json:"thumbnail"`
	OriginalUrl string   `json:"original_url"`
	Formats     []Format `json:"formats"`
	Format      string   `json:"format"`
	Width       int      `json:"width"`
	Height      int      `json:"height"`
	URL         string   `json:"url"`
	Ext         string   `json:"ext"`
}

type Format struct {
	Ext      string `json:"ext"`
	FormatId string `json:"format_id"`
	Acodec   string `json:"acodec"`
	Vcodec   string `json:"vcodec"`
}

func (m *MediaInfo) GetThumbnail() (string, error) {
	if m.Thumbnail == "" {
		return "", errors.New("no thumbnail URL provided")
	}

	thumbId := uuid.New().String()

	filename := fmt.Sprintf("", "%s.jpg", thumbId)
	thumbnailPath := filepath.Join("", filename)

	resp, err := http.Get(m.Thumbnail)
	if err != nil {
		return "", err
	}

	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("failed to download thumbnail: %s", resp.Status)
	}

	out, err := os.Create(thumbnailPath)
	if err != nil {
		return "", err
	}
	defer out.Close()

	_, err = io.Copy(out, resp.Body)
	if err != nil {
		return "", err
	}

	return thumbnailPath, nil
}

func Download(mediaInfo MediaInfo, format string) (string, error) {
	input := mediaInfo.OriginalUrl
	fileId := uuid.New().String()
	filePath := filepath.Join(os.TempDir(), fileId) + "." + "%(ext)s"

	var cmd *exec.Cmd
	if isURL(input) && UrlExists(input) {
		cmd = exec.Command("yt-dlp", "--get-filename", "-f", format, "-o", filePath, input)

		var out bytes.Buffer
		cmd.Stdout = &out
		cmd.Stderr = &out

		if err := cmd.Run(); err != nil {
			return "", fmt.Errorf("error retrieving filename: %w", err)
		}

		downloadCmd := exec.Command("yt-dlp", "--quiet", "-f", format, "-o", filePath, input)
		if err := downloadCmd.Run(); err != nil {
			return "", fmt.Errorf("error downloading: %w", err)
		}

		return strings.TrimSpace(out.String()), nil
	}

	return "", fmt.Errorf("invalid URL or media info")
}

func GetMediaInfo(input string, mediaInfo *MediaInfo) error {
	var cmd *exec.Cmd
	if isURL(input) && UrlExists(input) {
		cmd = exec.Command("yt-dlp", "-j", "--no-warnings", input)
	} else {
		cmd = exec.Command("yt-dlp", "ytsearch:"+input, "-j", "--no-warnings")
	}

	var out bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = &out

	if err := cmd.Run(); err != nil {
		return fmt.Errorf("error getting media info: %w", err)
	}

	if err := json.Unmarshal(out.Bytes(), &mediaInfo); err != nil {
		return fmt.Errorf("failed to unmarshal media info: %w", err)
	}

	return nil
}
