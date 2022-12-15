FROM python:3.10-slim-buster
RUN apt-get update && apt-get -y install cron

WORKDIR /code

COPY . .

COPY lru_cleaner /etc/cron.d/hello-cron

RUN crontab /etc/cron.d/hello-cron
