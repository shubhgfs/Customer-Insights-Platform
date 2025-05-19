# Use official Python image
FROM python:3.12.10-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all necessary files
COPY . .

# Expose the port Streamlit or your app might use (default: 8000 or 8501)
EXPOSE 7777

# Run the app using uvicorn
CMD ["python", "agno_test.py"]
