package helpers

import (
	"context"
	"encoding/json"
	"strconv"

	"github.com/redis/go-redis/v9"
)

func AddToQueue(r *redis.Client, chatId int64, data *Queue) error {
	s := strconv.FormatInt(chatId, 10)
	mj, err := json.Marshal(data)
	if err != nil {
		return err
	}

	_, err = r.Set(context.Background(), s, mj, 0).Result()
	if err != nil {
		return err
	}

	return nil
}

func GetInQueue(r *redis.Client, chatId int64) (*Queue, error) {
	s := strconv.FormatInt(chatId, 10)

	k, err := r.Get(context.Background(), s).Result()
	if err != nil {
		return nil, err
	}

	var queue Queue
	err = json.Unmarshal([]byte(k), &queue)
	if err != nil {
		return nil, err
	}

	return &queue, nil
}

func RemoveQueue(r *redis.Client, chatId int64) error {
	s := strconv.FormatInt(chatId, 10)

	_, err := r.Del(context.Background(), s).Result()
	if err != nil {
		return err
	}

	return nil
}
