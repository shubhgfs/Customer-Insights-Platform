# Use the latest official Python 3.13 image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose the default port for Streamlit (if used) or Flask
EXPOSE 8501

# Change this line to match your actual main script
CMD ["python", "app.py"]
