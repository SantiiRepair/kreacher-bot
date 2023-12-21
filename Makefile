.PHONY: build clear install

build:
	docker compose build

clear:
	docker compose down --volumes

docker: clear build
	docker compose up -d --remove-orphans

install:
	go mod tidy

format:
	go fmt

start:
	cd kreacher && go run . && cd ..

