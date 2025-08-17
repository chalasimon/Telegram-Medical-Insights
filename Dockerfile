# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Load environment variables from .env file
#ENV PYTHONUNBUFFERED=1

# Command to run the application (modify as needed)
#CMD ["python", "your_script.py"]