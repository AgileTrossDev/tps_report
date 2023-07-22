# Use the official Ubuntu base image
FROM ubuntu:latest

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# Update and install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt /app/

# Install Python dependencies
RUN python3 -m venv venv
RUN . venv/bin/activate && pip install -r requirements.txt

# Copy the entire project directory to the container
COPY . /app/

# Expose the Django development server port
EXPOSE 8000

# Start the Django development server
CMD ["venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]