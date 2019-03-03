FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

ENV PYTHONPATH /code/fried_chicken
ENV DJANGO_SETTINGS_MODULE fried_chicken.settings.base

COPY . /code/
