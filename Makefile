.PHONY: build clean

build:
	docker compose build

clean:
	docker compose down --volumes

docker:
	docker compose up -d --remove-orphans

install:
	cd kreacher && go mod tidy && cd ..

format:
	cd kreacher && go fmt && cd ..

start:
	cd kreacher && go run . && cd ..

setvars:
	export $(cat .env | xargs)