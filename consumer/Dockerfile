# Use the official Python image as the base image
FROM python:3.9

# Install Python
RUN apt-get update && apt-get install -y python3

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python script and any other necessary files into the container
COPY main.py .

# Command to run your Python application
CMD ["python", "main.py"]