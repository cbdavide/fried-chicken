FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /project

COPY requirements.txt /project/
RUN pip install -r /project/requirements.txt

ENV PYTHONPATH /project/code/
ENV DJANGO_SETTINGS_MODULE fried_chicken.settings.base

RUN mkdir /project/code
WORKDIR /project/code

COPY fried_chicken/ /project/code/
