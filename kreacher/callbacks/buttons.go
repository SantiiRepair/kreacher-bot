package callbacks

import tele "gopkg.in/telebot.v3"

var (
	selector  = &tele.ReplyMarkup{}
	prevBtn   = selector.Data("", "prev")
	pauseBtn  = selector.Data("", "pause")
	resumeBtn = selector.Data("", "resume")
	nextBtn   = selector.Data("", "next")
	pingBtn   = selector.Data("", "ping")
)
