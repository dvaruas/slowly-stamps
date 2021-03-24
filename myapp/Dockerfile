FROM python:3.8-slim
LABEL maintainer="Saurav Das [saurav.das37@gmail.com]"

WORKDIR /app

COPY . .
ENV FLASK_ENV=production

RUN pip install -r requirements.txt
