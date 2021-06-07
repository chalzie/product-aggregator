FROM python:3.7-alpine

COPY ./app /app
WORKDIR /app

RUN apk add bash libffi-dev postgresql-dev postgresql gcc python3-dev musl-dev libxml2-dev libxslt-dev --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/community/ --allow-untrusted

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

EXPOSE 80

