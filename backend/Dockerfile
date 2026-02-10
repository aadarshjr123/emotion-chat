FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libffi-dev libssl-dev postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY app ./app
COPY wait-for-db.sh ./
COPY scripts ./scripts

# Make the wait script executable
RUN chmod +x wait-for-db.sh

EXPOSE 8000

COPY static/ /app/static/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
