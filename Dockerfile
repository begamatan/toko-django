FROM python:alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update \
    && apk add \
    build-base \
    gcc musl-dev mariadb-connector-c-dev \
    bash git openssh \
    mysql \
    mysql-client

RUN mkdir /usr/src/app

WORKDIR /usr/src/app

COPY src/requirements.txt .

RUN pip install -r requirements.txt

COPY ./src .

# Expose port 8000 to the outside world
EXPOSE 8000
