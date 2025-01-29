FROM python:3.11-alpine

WORKDIR /app

COPY ./parallel-thread-pool.py ./app.py

ENV SAMPLES=5
ENV WORKLOAD=100000
ENV NUM_WORKERS=10

CMD ["python", "app.py"]
