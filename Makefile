export PATH := $(HOME)/.local/bin:$(PATH)
VENV_PATH := $(shell pwd)/.venv
VENV_ACTIVATE := $(VENV_PATH)/bin/activate


start_local_db:
	docker compose -f docker-compose.yaml up db -d

db_tests:
	. $(VENV_ACTIVATE) && \
	poetry run coverage run -m pytest -v -s && coverage report --show-missing

build:
	poetry run sudo docker compose -f docker-compose.yaml up -d

