PORT ?= 9000
WORKERS ?= 5
.PHONY: install start-dev start lint build

install:
	poetry install

start:
	poetry run flask --app page_analyzer:app --debug run


start-production:
	poetry run gunicorn --daemon -w $(WORKERS) -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	poetry run flake8 .

build:
	./build.sh
