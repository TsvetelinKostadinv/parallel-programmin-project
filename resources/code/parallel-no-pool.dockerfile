FROM python:3.11-alpine

WORKDIR /app

COPY ./parallel-no-pool.py ./app.py

ENV SAMPLES=5
ENV ITERATIONS=1000000

CMD ["python", "app.py"]
