## E-MENU APP

### Pre-requirements
* docker and docker-compose are installed:
    - [docker install](https://docs.docker.com/engine/install/)
    - [docker-compose install](https://docs.docker.com/compose/install/)

**NOTE**
If you want to run the app on windows and use make commands you will have to install [choco](https://chocolatey.org/install) and next run the command `choco install make` to install `make` after the installation you will have to restart your computer.

### Makefile commands
1. build - build docker image
2. run - run app by docker compose `run` command
3. start - run app by docker compose `up -d` command
4. stop - stop containers
5. clean - stop and remove containers, networks and named volumes
6. makemigrations - run `makemigrations` command
7. migrate - run `migrate` command
8. bash - attach docker shell
9. lint - run `black`, `isort` and `pflake8`
10. coverage - run unit tests and report test coverage
11. createsuperuser - run `createsuperuser` command
12. run_test_email_command - run commnd to test sending emails
13. load_data - load test data

### Run application
1. Copy `example_env.env` data, create `.env` in the same place as `example_env.env` file and paste data from `example_env.env` file to new `.env` file
2. Use `make build` command and next `make start` or `make run` command
3. To load test data use `make load_data` command (superuser credentials: `admin:admin`)
4. To run tests use `make coverage` command


### Django crontab commands
1. To show lunched crons use `docker-compose exec emenu python manage.py crontab show`
2. To run manually the cron job use `docker-compose exec emenu python manage.py <id_from_previous_command>`