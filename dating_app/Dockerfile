FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /dating_app

COPY requirements.txt /dating_app/requirements.txt
COPY wait_for_it.sh /dating_app/wait_for_it.sh

RUN chmod +x ./wait_for_it.sh
RUN pip3 install -r requirements.txt

COPY . /dating_app
