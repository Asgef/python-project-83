install:
	poetry install

dev:
	poetry rum flask -app page_analizer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analizer:app

lint:
	poetry run flake8 .
