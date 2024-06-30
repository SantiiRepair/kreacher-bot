.PHONY: build-docker clean-docker

build-docker:
	docker compose build

clean-docker:
	docker compose down --volumes

docker:
	docker compose up -d --remove-orphans

install:
	cd kreacher && go mod tidy && cd ..

format:
	@find kreacher -mindepth 1 -maxdepth 1 -type d -exec sh -c 'cd {} && go fmt' \;

start:
	cd kreacher && go run . && cd ..

senv:
	export $(cat .env | xargs)