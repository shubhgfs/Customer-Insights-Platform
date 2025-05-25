# Use the latest official Python 3.13 slim image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies for building wheels (C++ compiler etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project into the container
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose default port (Streamlit: 8501, Flask default: 5000 if applicable)
EXPOSE 8501

# Run the app using Streamlit
CMD ["streamlit", "run", "login.py", "--server.port=8501", "--server.address=0.0.0.0"]
