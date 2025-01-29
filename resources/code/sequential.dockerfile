FROM python:3.11-alpine

WORKDIR /app

COPY ./sequential.py ./app.py

ENV SAMPLES=5
ENV ITERATIONS=1000000

CMD ["python", "app.py"]
