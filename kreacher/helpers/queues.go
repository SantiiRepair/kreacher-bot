package helpers

import (
	"context"
	"encoding/json"
	"strconv"

	"github.com/redis/go-redis/v9"
)

// Adds a new item to the queue in Redis.
func AddToQueue(r *redis.Client, chatId int64, params *Queue) (int, error) {
	s := strconv.FormatInt(chatId, 10)

	k, err := r.Get(context.Background(), s).Result()
	if err != nil && err != redis.Nil {
		return 0, nil
	}

	data := &queue{
		Requester:     params.Requester,
		AudioStream:   params.AudioStream,
		VideoStream:   params.VideoStream,
	}

	var result []queue
	if k != "" {
		err = json.Unmarshal([]byte(k), &result)
		if err != nil {
			return 0, err
		}

		data.NumberInQueue = result[len(result)-1].NumberInQueue + 1
	} else {
		data.NumberInQueue = 1
	}

	result = append(result, *data)

	mj, err := json.Marshal(result)
	if err != nil {
		return 0, err
	}

	_, err = r.Set(context.Background(), s, mj, 0).Result()
	if err != nil {
		return 0, err
	}

	return data.NumberInQueue, nil
}

// Returns the element in the queue for a given chatId.
func GetQueue(r *redis.Client, chatId int64) ([]Queue, error) {
	s := strconv.FormatInt(chatId, 10)

	k, err := r.Get(context.Background(), s).Result()
	if err == redis.Nil {
		return nil, nil
	} else if err != nil {
		return nil, err
	}

	var queue []Queue
	err = json.Unmarshal([]byte(k), &queue)
	if err != nil {
		return nil, err
	}

	return queue, nil
}

// Deletes the queue for a given chatId.
func PopQueue(r *redis.Client, chatId int64) error {
	s := strconv.FormatInt(chatId, 10)

	_, err := r.Del(context.Background(), s).Result()
	return err
}

// Deletes the queue for a given chatId.
func DeleteQueue(r *redis.Client, chatId int64) error {
	s := strconv.FormatInt(chatId, 10)

	_, err := r.Del(context.Background(), s).Result()
	return err
}
