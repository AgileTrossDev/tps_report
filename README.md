# Temperature Processor Service (TPS) Report 
Temperature Processor Service Report, or TPS Report for short, is a system of microservices running in Docker.  It consists of a headless consumer service that subscribes to a websocket streaming temperature telemetry is responsible for populating an external InfluxDB with the time-series data representing the Temperature measurements. The InfluxDB runs in the timeseries_temperature_db Docker and serves as the backing-store for the system. A Django Project called TPS hosts the Temperature API Application that implements a GraphQL API using Graphene to allow users the ability to query the Temperature measurements streamed in the InfluxDB. 

```Yeah. It's just we're putting new coversheets on all the TPS reports before they go out now. So if you could go ahead and try to remember to do that from now on, that'd be great. All right?```

# TODO
- Deploy TPS Project to Docker
- Deploy temperature_reader to Docker
- Change the default settings of the influxdb



# Services
TPS is easily lanuched and managed by the docker-compose.yml file.

Build and launch service within Docker
```docker-compose up --build```


## satellite-temperature

## Consumder
Connects




## Temperature Reader
Simple script meant as a development tool.  It will execute a loop with a 2 second sleep in between queries to the Timeseries Temperature DB.  The results of the query we will printed to stdout.



 - report  - GraphQL API to accessing temperature data.  (Has People Skills. Talks to the customer, so the software engineers don't have to)

 This app will handle the frontend part of your application, including the GraphQL API, views, templates, and any client-side logic or JavaScript code. You can use Graphene or any other library to implement the GraphQL API in this app.

 - consumer - Ingests data stream and stores in database
 
 This app will handle the backend part of your application that consumes the data stream. Depending on your requirements, this app might include background tasks, data processing, and interacting with the data stream source. You can use Django Channels or any other library that supports asynchronous processing for consuming the data stream.
 

# Assignment
## Must Haves
- Let's get fancy, and use modern Python (>= 3.7).
- A Dockerfile and/or docker-compose.yml file should be provided, to make the whole setup portable and easy-
to-use.
- The service should be built using Django. Additional libraries and database solution can be selected at will.
- A README.md file is expected, to detail the chosen solution, and how to run it.
- Relevant unit tests should be provided (using pytest).
- Use Python type annotations.

## Tasks:
- Build a Django app which can store temperature readings (a timestamp and a value) in the database.
- Subscribe to the temperature feed to continuously populate the
database.
- Build a GraphQL API exposing the following operations:
  - a query that returns the current temperature (last emitted temperature)
  - a query that returns the minimum and maximum temperature within a time window provided via a before
and/or after timestamp as argument

## Setup
### Dependencies
- Docker
- Docker-compose
- Python 3.9
- pip

### Pip Install
Use pip to install requirements:
`pip install -r requirements.txt`

***NOTE** Requirement versions are not constrained at the moment.

## Launching the Service


## Accessing

``http://localhost:8000/```

# Django Setup

## django-admin startproject

```django-admin startproject tps .```

Used to create the temp_processor_project.
- manage.py - CLI Tool for managing Django
- settings.py - Setting for Django
- urls.py - URL Configuration of the project
- wsgi.py - Entry point for WSGI Servers (Gunicorn)
- asgi.py - Entry Point for ASGI-based deployement (Daphne/WebSocket)

## python manage.py startap

```python manage.py startap report .```
```python manage.py startap consumer .```

USed to setup the Application Module for the Django App.  In this Project, we are building the Temp Processor Application.  Django Projects may have several different Apps.  Using this utility a directory is created for the App containing the following files:

- __init__.py: An empty file that marks the directory as a Python package.
- admin.py: This file is used to register models with the Django admin interface, allowing you to manage app-specific data via the admin panel.
- apps.py: This file includes the app configuration. You can customize app behavior using this file, but the default settings are usually sufficient for most cases.
- models.py: This is where you define your app's data models using Django's model classes. Models represent the database schema and structure of your app's data.
- tests.py: This file is where you can write unit tests for your app's functionality.
- views.py: This is where you define your app's view functions, which handle HTTP requests and render templates or return JSON responses.
- urls.py: The URL configuration file for the app. It defines the app-level URL patterns and their corresponding view functions.
- migrations/: This directory stores database migration files generated by Django when you create or modify models.


***Registering the App:*** Once the app is created, you need to register it in the project's settings to ensure Django recognizes and includes it. To do this, open the project's settings.py file and add the app name to the INSTALLED_APPS list.


# Docker


***Dockerfile*** -  Uses latest Ubuntu image and Python 3 environment for the service.

***docker-compose*** - Runtime information for the temperature_feed service, mapping Port 8000 to the Django Service in the container.





