# Density.io Fullstack Homework

I opted for Django, which I've never used before. I tried to stick to the framework's conventions, but I probably didn't follow all the best common practices due to a lack of familiarity.

The assignment asked for a DB containing sensors and heartbeats. I view the heartbeat as an attribute of the sensor. If the assignment were to store metrics from the sensor, I would have included a table for metrics. Ideally, they would be stored in something designed for time-series data, like Timescale DB or InfluxDB.

The app exposes `GET /heartbeat`, which takes the MAC address of the sensors and updates the sensor's `last_heartbeat` with the current time.

The index page (`GET /`) displays a grid of sensors updated every minute via a fetch to `GET /sensors`. Sensors added after the page load are not added to the grid. I would have liked to support this but ran out of time. To accomplish this, I would move all the grid logic into JS and fetched the sensors on page load.

I was not able to add user notifications. This is a hard problem to do at scale and avoid duplicate/missing notifications. One open question is how to notify the user. SMS, Email, in-browser notifications? Each has it's own challenges and infrastructure needs. I would have implemented an additional service that polled the database looking for sensors with a heartbeat older than 10 minutes that hasn't already sent a notification recently. Notifications would go on a fanout queue. Notification workers would process the queue. For SMS and/or email, I would use SNS or SES to send the notification. In-browser notifications would require websockets or a status attribute on the sensor data being polled, which would trigger the in-browser notification.

## Setup

```
$ docker-compose up -d db
$ docker-compose up migrations
$ docker-compose run web python manage.py createsuperuser
<Fill out user details>
```

## Running

```
$ docker-compose up 
```

The app can be accessed at http://localhost:8000/

## Helpful commands

#### Heartbeat sensor with curl
```
curl -X POST -H "Content-Type: application/json" -d '{"mac_address":"02:00:00:00:00:00"}'  http://localhost:8000/heartbeat
```

#### Get sensors with curl
```
curl http://localhost:8000/sensors
```

#### Connecting to DB

```
docker-compose exec -e PGPASSWORD=postgres db psql -h db -U postgres postgres
```

#### Run migrations
```
docker-compose run web python manage.py makemigrations sensors
```
