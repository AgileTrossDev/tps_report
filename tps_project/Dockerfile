# Dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt manage.py /temperature_api/ /tps_project/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]