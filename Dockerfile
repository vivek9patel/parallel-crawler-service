# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 python:3.12-slim

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "index:app", "--name", "crawler-service", "--max-requests", "100", "--capture-output"]