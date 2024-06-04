FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY worker.py .

RUN useradd -m worker
USER worker

CMD ["python", "worker.py"]
