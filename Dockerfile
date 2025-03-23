# Use official Python image as base
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory
COPY . .

# Expose internal port
EXPOSE 8501

# Run the Streamlit app on internal port 8501
CMD ["streamlit", "run", "login.py", "--server.port=8501", "--server.address=0.0.0.0"]
