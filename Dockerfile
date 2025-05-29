FROM python:3.10-slim

RUN apt-get update;

ENV PYTHONUNBUFFERED=1
RUN mkdir /app

ADD requirements.txt /app
ADD scripts/init.sh /app

WORKDIR /app

RUN chmod +x *.sh

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /app