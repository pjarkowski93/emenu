.PHONY: build run start stop clean makemigrations migrate bash lint coverage createsuperuser

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
	docker-compose exec emenu black . && isort . && pflake8 .

tests:
	docker-compose exec emenu coverage run manage.py test .

coverage:
	docker-compose exec emenu coverage run manage.py test .
	docker-compose exec emenu coverage report

createsuperuser:
	docker-compose exec emenu python manage.py createsuperuser