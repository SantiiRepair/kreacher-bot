package scrapers

import (
	"context"
	"fmt"
	"time"

	"github.com/chromedp/chromedp"
)

// SearchImageOpts represents image search options.
// By default, returns the image string path if the goal is achieved.
// However, if 'ReturnAsBytes' is set to 'true', it will return the image in bytes.
//
// You can also specify the `NumberOfImages` to search according to the query and the desired image resolution range using 'MinResolution' and 'MaxResolution'.
type SearchImageOpts struct {
	NumberOfImages int
	MinResolution  []int
	MaxResolution  []int
	ReturnAsBytes  bool
	OutputImage    string
}

func GetImageFromQuery(ctx context.Context, query string, opts SearchImageOpts) (interface{}, error) {
	ctx, cancel := chromedp.NewContext(ctx)

	defer cancel()

	var htmlContent string

	url := fmt.Sprintf("https://www.google.com/search?q=%s&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947", query)

	if err := chromedp.Run(ctx,
		chromedp.Navigate(url),
		chromedp.Sleep(2*time.Second),
		chromedp.OuterHTML("html", &htmlContent),
	); err != nil {
		return nil, err
	}

	return htmlContent, nil
}
