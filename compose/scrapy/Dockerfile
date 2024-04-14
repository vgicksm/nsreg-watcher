# syntax=docker/dockerfile:1
FROM python:3.11
COPY . /app/
COPY .env /app/
WORKDIR /app
RUN apt-get clean && rm -rf /var/lib/apt/lists/* && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys
RUN apt-get update
RUN apt-get install -y gettext-base
RUN sh install.sh
CMD ["python", "src/telegram_bot"]
