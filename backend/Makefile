.PHONY: app debug app-down install

DC = docker-compose
ENV = --env-file .env
APP_FILE = docker-compose.yml
APP_CONTAINER = main-backend


app:
	sudo $(DC) -f $(APP_FILE) $(ENV) up --build -d

app-down:
	sudo $(DC) -f $(APP_FILE) down

debug:
	python run.py

install:
	pip install poetry
	poetry update