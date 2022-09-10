FROM python:slim
LABEL maintainer="Saurav Das [saurav.das37@gmail.com]"

WORKDIR /app

COPY . .
ENV USE_DEV=false

RUN pip install -r requirements.txt
