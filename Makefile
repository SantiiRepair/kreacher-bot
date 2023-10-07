.PHONY: install

run-container:
	docker-compose up -d --build

install:
	pip install --no-deps -U pytgcalls==3.0.0.dev24 tgcalls==3.0.0.dev6
	pip install -r requirements-dev.txt
	pip install -r requirements.txt

format:
	black .

lint:
	pylint --recursive yes --jobs=4 .

session:
	python ./session/session.py

start: install
	python -m bot

