package helpers

import (
	"context"
	"encoding/json"
	"strconv"
	"strings"

	"github.com/pkg/errors"
	"github.com/redis/go-redis/v9"
	"santiirepair.dev/kreacher/core"
)

type Queue struct {
	Active        bool   `json:"active"`
	Requester     int64  `json:"requester"`
	OriginalUrl   string `json:"original_url"`
	StreamType    string `json:"stream_type"`
	Command       string `json:"command"`
	NumberInQueue int    `json:"number_in_queue"`
}

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

const (
	cacheExpiration = 0 // no expiration
)

// Changes the active queue for the given chatId.
//
// It returns the deactivated queue and an error if any.
func MovePlayList(chatId int64, switchTo string) (*Queue, error) {
	s := strconv.FormatInt(chatId, 10)

	queuesBytes, err := core.R.Get(context.Background(), s).Bytes()
	if err == redis.Nil {
		return nil, nil
	} else if err != nil {
		return nil, err
	}

	var queues []Queue
	err = json.Unmarshal(queuesBytes, &queues)
	if err != nil {
		return nil, err
	}

	if len(queues) < 2 {
		return nil, errors.New("not enough streams to move")
	}

	activeQueueIndex := -1
	for i, queue := range queues {
		if queue.Active {
			activeQueueIndex = i
			break
		}
	}

	if activeQueueIndex == -1 {
		return nil, errors.New("no active queue found")
	}

	queues[activeQueueIndex].Active = false

	switch strings.ToLower(switchTo) {
	case "next":
		if activeQueueIndex < len(queues)-1 {
			queues[activeQueueIndex+1].Active = true
		} else {
			return nil, errors.New("no next queue found")
		}
	case "prev":
		if activeQueueIndex > 0 {
			queues[activeQueueIndex-1].Active = true
		} else {
			return nil, errors.New("no previous queue found")
		}
	default:
		return nil, errors.New("invalid switchTo parameter")
	}

	updatedQueuesBytes, err := json.Marshal(queues)
	if err != nil {
		return nil, err
	}

	_, err = core.R.Set(context.Background(), s, updatedQueuesBytes, cacheExpiration).Result()
	if err != nil {
		return nil, err
	}

	return &queues[activeQueueIndex], nil
}

// Deletes the queue for a given chatId.
func DeleteQueue(chatId int64) error {
	s := strconv.FormatInt(chatId, 10)

	_, err := core.R.Del(context.Background(), s).Result()
	return err
}
