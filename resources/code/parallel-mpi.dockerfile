FROM python:3.11-alpine

WORKDIR /app

RUN pip install mpi4py
RUN apk add --no-cache openmpi
RUN export PATH=/usr/lib/openmpi/bin:$PATH

COPY ./parallel-mpi.py ./app.py

ENV SAMPLES=5
ENV ITERATIONS=100000

CMD ["mpiexec", "-n 8", "python", "app.py"]
