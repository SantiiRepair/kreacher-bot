.PHONY: build clear install

build:
	docker compose build

clear:
	docker compose down --volumes

docker: clear build
	docker compose up -d --remove-orphans

install:
	cd kreacher && go mod tidy && cd ..

format:
	go fmt

start:
	cd kreacher && go run . && cd ..

