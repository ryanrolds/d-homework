# Density.io Fullstack Homework

## Setup

```
$ docker-compose up db
$ docker-compose up migrations
$ docker-compose run web python manage.py createsuperuser
... Fill out user details
```

## Running

```
$ docker-compose up 
```

The app can be accessed at http://localhost:8000/

### Create super user

```
$ docker-compose run web python manage.py createsuperuser
```



## Notes and helpful commands

```
docker-compose exec db psql -h db -U postgres postgres
docker-compose run web python manage.py makemigrations sensors
docker-compose run web python manage.py sqlmigrate sensors 0001
```

