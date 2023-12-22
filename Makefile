.PHONY: setvars build clean install

build:
	docker compose build

clean:
	docker compose down --volumes

docker: clean build
	docker compose up -d --remove-orphans

install:
	cd kreacher && go mod tidy && cd ..

format:
	cd kreacher && go fmt && cd ..

start:	setvars
	cd kreacher && go run . && cd ..

setvars:
	export $(cat .env | xargs)