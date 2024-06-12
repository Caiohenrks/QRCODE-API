FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app.py .
COPY ./templates ./templates
COPY ./static ./static
COPY ./instance ./instance

RUN adduser --disabled-login --gecos '' appuser \
    && chown -R appuser:appuser /app

USER appuser

CMD ["python", "app.py"]
