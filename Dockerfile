FROM python:3.8-slim
LABEL maintainer="Saurav Das [saurav.das37@gmail.com]"

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]
