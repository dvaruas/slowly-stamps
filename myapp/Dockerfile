FROM python:slim
LABEL maintainer="Saurav Das [saurav.das37@gmail.com]"

WORKDIR /app

COPY . .
ENV FLASK_ENV=production

RUN pip install -r requirements.txt
