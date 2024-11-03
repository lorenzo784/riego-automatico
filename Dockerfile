FROM python:3.12.4-alpine3.20

RUN pip install --upgrade pip --no-cache-dir

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app

RUN chmod +x /app/server-entrypoint.sh
RUN chmod +x /app/worker-entrypoint.sh