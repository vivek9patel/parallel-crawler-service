FROM python:3.12-slim

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "index:asgi_app", "--name", "crawler-service", "--max-requests", "1",  "--worker-class", "uvicorn.workers.UvicornWorker", "--access-logfile", "access_logs.log", "--error-logfile", "error_logs.log", "--capture-output"]