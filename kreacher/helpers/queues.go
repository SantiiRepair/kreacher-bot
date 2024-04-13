package helpers

import (
	"context"
	"encoding/json"
	"strconv"
	"strings"

	"github.com/redis/go-redis/v9"
	"santiirepair.dev/kreacher/core"
)

// Adds a new item to the queue in Redis.
func AddToPlayList(chatId int64, data *Queue) (int, error) {
	s := strconv.FormatInt(chatId, 10)

	k, err := core.R.Get(context.Background(), s).Result()
	if err != nil && err != redis.Nil {
		return 0, nil
	}

	var result []Queue
	if k != "" {
		err = json.Unmarshal([]byte(k), &result)
		if err != nil {
			return 0, err
		}

		data.NumberInQueue = result[len(result)-1].NumberInQueue + 1
	} else {
		data.Active = true
		data.NumberInQueue = 0
	}

	if data.VideoSource != "" {
		data.StreamType = "video"
	} else {
		data.StreamType = "audio"
	}

	result = append(result, *data)

	mj, err := json.Marshal(result)
	if err != nil {
		return 0, err
	}

	_, err = core.R.Set(context.Background(), s, mj, 0).Result()
	if err != nil {
		return 0, err
	}

	return data.NumberInQueue, nil
}

// Changes the active queue for the given chatId.
func MovePlayList(chatId int64, switchTo string) (*Queue, error) {
	s := strconv.FormatInt(chatId, 10)

	k, err := core.R.Get(context.Background(), s).Result()
	if err == redis.Nil {
		return nil, nil
	} else if err != nil {
		return nil, err
	}

	var queues []Queue
	err = json.Unmarshal([]byte(k), &queues)
	if err != nil {
		return nil, err
	}

	for i, queue := range queues {
		if queue.Active {
			queues[i].Active = !queues[i].Active
			if strings.ToLower(switchTo) == "next" {
				if i < len(queues)-1 {
					queues[i+1].Active = true
				}
			} else {
				if i > 0 {
					queues[i-1].Active = true
				}
			}

			mj, err := json.Marshal(queues)
			if err != nil {
				return nil, err
			}

			_, err = core.R.Set(context.Background(), s, mj, 0).Result()
			if err != nil {
				return nil, err
			}

			return &queues[i], nil
		}
	}

	return nil, nil
}

// Deletes the queue for a given chatId.
func DeleteQueue(r *redis.Client, chatId int64) error {
	s := strconv.FormatInt(chatId, 10)

	_, err := r.Del(context.Background(), s).Result()
	return err
}
