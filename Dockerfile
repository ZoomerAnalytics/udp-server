FROM python:3.6.0-slim
MAINTAINER Zoomer Analytics LLC <info@zoomeranalytics.com>

WORKDIR /
RUN mkdir app
WORKDIR /app
COPY . /app
WORKDIR /app

CMD ["python", "app.py"]
