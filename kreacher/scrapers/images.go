package scrapers

import (
	"context"
	"fmt"
	"time"

	"github.com/chromedp/chromedp"
)

type ImageFinder struct {
	target         string
	numberOfImages int
}

// Start a new search engine with the given options
func NewImageFinder(target string, numberOfImages int) *ImageFinder {
	return &ImageFinder{
		target:         target,
		numberOfImages: numberOfImages,
	}
}

// Searches for high resolution images in Yahoo Search and returns the url of the target image
func (finder *ImageFinder) FindImageURLs() ([]string, error) {
	opts := append(chromedp.DefaultExecAllocatorOptions[:],
		chromedp.Flag("headless", true),
	)

	allocCtx, cancelAlloc := chromedp.NewExecAllocator(context.Background(), opts...)
	defer cancelAlloc()

	ctx, cancel := chromedp.NewContext(allocCtx)
	defer cancel()

	if err := chromedp.Run(ctx,
		chromedp.Navigate(fmt.Sprintf("https://images.search.yahoo.com/search/images;?fr2=sb-top-images.search&p=%s", finder.target)),
		chromedp.Sleep(3*time.Second),
	); err != nil {
		return nil, err
	}

	var imageUrls []string
	searchString := `//*[@id="results"]/div/ul/li[%d]/a/img`

	for i := range finder.numberOfImages {
		var imgSrc string

		if err := chromedp.Run(ctx,
			chromedp.Click(fmt.Sprintf(searchString, i+1), chromedp.BySearch),
			chromedp.Sleep(1*time.Second),
			chromedp.AttributeValue(`//*[@id="img"]`, "src", &imgSrc, nil),
			chromedp.Click(`//*[@class="close"]`, chromedp.BySearch),
			chromedp.Sleep(1*time.Second),
		); err != nil {
			return nil, err
		}

		if imgSrc != "" && !contains(imageUrls, imgSrc) {
			imageUrls = append(imageUrls, imgSrc)
		}

	}

	return imageUrls, nil
}

func contains(slice []string, item string) bool {
	for _, s := range slice {
		if s == item {
			return true
		}
	}
	return false
}
