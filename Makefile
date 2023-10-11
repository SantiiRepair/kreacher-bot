.PHONY: install

docker:
	docker-compose up -d --build --remove-orphans

docker-down:
	docker-compose down --volumes

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

