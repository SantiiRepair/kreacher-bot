.PHONY: build clear install

build:
	docker-compose build

clear:
	docker-compose down --volumes

docker: clear build
	docker-compose up -d --remove-orphans

install:
	pip install -r requirements.txt

format:
	black .

lint:
	pylint --recursive yes --jobs=4 .

session-string:
	python ./session/session.py

start:
	python -m bot

