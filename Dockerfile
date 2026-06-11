FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src

ENV PYTHONPATH=/app
EXPOSE 8000

# no secrets in the image; config comes from env / configmap
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
