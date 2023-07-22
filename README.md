# Temperature Processor Service (TPS)
Backend Service that consumes temperature feed and implements a GraphQL API to create Temperature Processor Service Report, or TPS Report for short.

```Yeah. It's just we're putting new coversheets on all the TPS reports before they go out now. So if you could go ahead and try to remember to do that from now on, that'd be great. All right!``

This service deploys to a Docker Container running TPS Django Project with the TPS App.


## Setup
Use pip to install requirements:
`pip install -r requirements.txt`

***NOTE** Requirement versions are not constrained at the moment.

## Launching the Service
Build and launch service within Docker
`docker-compose up``

## Accessing

``http://localhost:8000/```




# Django Setup

## django-admin startproject
Used to create the temp_processor_project.
- manage.py - CLI Tool for managing Django
- settings.py - Setting for Django
- urls.py - URL Configuration of the project
- wsgi.py - Entry point for WSGI Servers (Gunicorn)
- asgi.py - Entry Point for ASGI-based deployement (Daphne/WebSocket)

## python manage.py startap
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





