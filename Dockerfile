FROM python:3.11.1-slim-bullseye

RUN apt-get update && apt-get -y install cron
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
