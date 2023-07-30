# Temperature Processor Service (TPS) Report 
Temperature Processor Service Report, or TPS Report for short, is a system of microservices running in Docker.  It consists of a headless Consumer service that subscribes to a websocket streaming temperature telemetry and is responsible for populating an external Influx Database with the time-series data representing the Temperature measurements. The InfluxDB runs in the timeseries_temperature_db Docker and serves as the backing-store for the system. A Django Project called TPS hosts the Temperature API Application that implements a GraphQL API using Graphene to allow users the ability to query the Temperature measurements streamed in the InfluxDB. 

```Yeah. It's just we're putting new coversheets on all the TPS reports before they go out now. So if you could go ahead and try to remember to do that from now on, that'd be great. All right?```

# TODO
- More Unit Tests
- Implement Functional Tests with Mocks
- Implement repeatable Integration Test


# Services
TPS is easily launched and managed by the docker-compose.yml file.

### How To

#### Test
```pytest```

#### Build and launch service within Docker
```docker-compose up --build```

#### Access the GraphQL API here
```http://localhost:8000/graphql```

#### Following along at home
```docker-compose logs -f```

#### Shut it down
```docker-compose down```

## satellite-temperature
Provied Docker that features a websocket streaming Temperature TLM.

## Consumer
Connects and subscribes via a websocket to the temperature telemetry feed provided by the satellite-temperature serivce.  The incoming data is written in real-time to the InfluxDb hosted in the timeseries_temperature_db Docker service.

### Design Decisions
This service was intentionally separated from the Django application hosting the query API.  This follows micro-service design best practices for modularity and allows for a more resillent system with fault isolation.  This allows for easier scalability and easier deployment in the future.

### TODO:
- Provide RESTful API to check health of consumer and manage the configuration to activate and connect to other streams

## TPS Project
Django Application implementing the GraphQL API for query Temperature Measurements stored in the InfluxDB hosted in the timeseries_temperature_db container.

### TODO:
- Connection Pool of InfluxDB Clients to improve performance and reduce overhead. (Not an issue yet)
- Current Temperature and Rolling Average


## timeseries_temperature_db
Container hosting the InfluxDB serving as the backing-store for the system.  Currently only the Temperature measuremeant is stored.  

### Desgin Decision
The data being processed in this system, time stamped temperature readings, is ideal for a time-series database.   Although Django does not support Influx natively, it was trivial to connect these two services.

### Debugging
Connect to Influx DB CLI. (Use the actual container ID.)
```
docker exec -it 53e47cc932c2 influx v1 shell
show databases
use my-bucket
show MEASUREMENTS
SELECT COUNT(*) temperature
SELECT * FROM temperature 
SELECT MIN(value) AS min_temp, MAX(value) AS max_temp FROM temperature WHERE time >= 1690587027046286592.0000000000 AND time <= 1690587049086376960.0000000000

```

## Temperature Reader
Simple script meant as a development tool.  It will execute a loop with a 2 second sleep in between queries to the Timeseries Temperature DB.  The results of the query we will printed to stdout.  This allows me to verify the flow of TLM from the Consumer to the Database.

***Not Deployed***

## Dev Tools
Tools to help with debug and manual testing
- iso8601_to_timestamp  ***Not Deployed***

## Setup

### Dependencies
Each Service within this System has it's own requirements.txt that should be pip installed.  This is performed automatically during the Docker Deploy.  A Development requirements-dev.txt is found at the root of the repository and contains dependencies to help with testing and linting.

### Pip Install

Use pip to install the development requirements:
`pip install -r requirements-dev.txt`




## Launching the Service


## Accessing

```http://localhost:8000/graphql```


***
# Smoke Test


## Current Temperature
`
query {
  currentTemperature {
    time
    value
   }
}
`


## Min and Max over a Time Range

```
query {
temperatureStatistics(after: "2023-07-28T13:00:00+00:00", before: "2023-07-28T14:00:00+00:00") {
min
max
}
}
```

## Last Two Seconds
```
query MyQuery {
  temperatureMeasurements {  
    time
    value
  }
}
```


