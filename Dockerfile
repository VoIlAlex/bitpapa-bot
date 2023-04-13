FROM python:3.11-alpine3.17

RUN apk update && apk add --update postgresql-dev gcc python3-dev musl-dev libffi-dev

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /app
COPY app /
