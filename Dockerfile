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

# Expose the default port for Streamlit
EXPOSE 8501

# Run the app using Streamlit
CMD ["streamlit", "run", "login.py", "--server.port=8501", "--server.address=0.0.0.0"]
