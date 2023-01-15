.PHONY: build run start stop clean makemigrations migrate bash lint

build:
	docker-compose build

run:
	docker-compose run --rm --service-ports emenu

start:
	docker-compose up -d

stop:
	docker-compose stop

clean:
	docker-compose down -v
	docker-compose rm -s -v

makemigrations:
	docker-compose exec emenu python manage.py makemigrations

migrate:
	docker-compose exec emenu python manage.py migrate

bash:
	docker-compose exec emenu bash

lint:
	black ./app && isort ./app && pflake8 ./app
