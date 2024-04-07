package helpers

import (
	"image"
	"image/png"
	"os"

	"github.com/fogleman/gg"
)

func GenThumbnail(text string) error {
	file, err := os.Open("")
	if err != nil {
		return err
	}

	img, _, err := image.Decode(file)
	if err != nil {
		return err
	}

	file.Close()

	dc := gg.NewContextForImage(img)

	dc.SetRGB(0, 0, 0)
	if err := dc.LoadFontFace("arial.ttf", 24); err != nil {
		return err
	}

	dc.DrawStringAnchored(text, 50, 50, 0, 0)
	out, err := os.Create("")
	if err != nil {
		return err
	}

	png.Encode(out, dc.Image())
	out.Close()

	return nil
}
