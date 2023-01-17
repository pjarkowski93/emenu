.PHONY: build run start stop clean makemigrations migrate bash lint coverage createsuperuser run_test_email_command load_data

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

run_test_email_command:
	docker-compose exec emenu python manage.py send_email --email test@test.com

load_data:
	docker-compose exec emenu python manage.py loaddata app/fixtures/user.json
	docker-compose exec emenu python manage.py loaddata emenu/fixtures/dish.json
	docker-compose exec emenu python manage.py loaddata emenu/fixtures/menu.json
	docker-compose exec emenu python manage.py loaddata emenu/fixtures/menu_dish_map.json