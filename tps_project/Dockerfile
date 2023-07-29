# Use the official Python image as the base image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory inside the container
WORKDIR /app

# Copy the Django project files to the container
COPY . /app/

RUN ls  

# Install Updates
#RUN apt-get update -y

# Install dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which your Django application will run (change it if necessary)
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]