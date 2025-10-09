FROM python:3.10-slim

RUN apt-get update;
RUN apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs

ENV PYTHONUNBUFFERED=1
RUN mkdir /app

ADD requirements.txt /app
ADD package.json /app
ADD scripts/init.sh /app

WORKDIR /app

RUN chmod +x *.sh

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN npm install
ADD . /app