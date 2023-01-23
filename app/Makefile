.PHONY: build run start stop clean migrate bash lint coverage createsuperuser run_test_send_email run_create_dish_email_notification load_data

docker_emenu := docker-compose exec emenu
manage_py := python manage.py

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

migrate:
	$(docker_emenu) $(manage_py) migrate

bash:
	$(docker_emenu) bash

lint:
	$(docker_emenu) black . && isort . && pflake8 .

tests:
	$(docker_emenu) coverage run manage.py test .

coverage:
	$(docker_emenu) coverage run manage.py test .
	$(docker_emenu) coverage report

createsuperuser:
	$(docker_emenu) $(manage_py) createsuperuser

run_test_send_email:
	$(docker_emenu) $(manage_py) send_email

run_create_dish_email_notification:
	$(docker_emenu) $(manage_py) create_dish_email_notification

load_data:
	$(docker_emenu) $(manage_py) loaddata app/fixtures/user.json
	$(docker_emenu) $(manage_py) loaddata emenu/fixtures/dish.json
	$(docker_emenu) $(manage_py) loaddata emenu/fixtures/menu.json
	$(docker_emenu) $(manage_py) loaddata emenu/fixtures/menu_dish_map.json
	$(docker_emenu) $(manage_py) loaddata notification/fixtures/notification.json
	$(docker_emenu) $(manage_py) loaddata notification/fixtures/notification_template.json