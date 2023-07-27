FROM python:3.11.2-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app/

copy ./requirements.txt ./requirements.txt

EXPOSE 8000

RUN pip install --upgrade pip && pip install -r requirements.txt && \
    adduser --disabled-password --no-create-home app

USER app