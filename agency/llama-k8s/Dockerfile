FROM python:3.11-slim

WORKDIR /app

# Install OS dependencies if needed, and clean up to keep image small
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY operator.py .

# Run the operations coordinator as the main entrypoint
CMD ["python", "operator.py"]
