# IWeatherMap - API

## Development Installation and Deployment to Docker Swarm

```bash

# Clone de repository
git clone https://github.com/gustavo-fonseca/iweathermap-api

# Go to project`s folder and copy .env.example to .env
cd ./iweathermap
cp .env.example .env

# Run docker-compose and make the initial migrations
docker-compose up -d
docker exec iweathermap_backend python manage.py makemigrations
docker exec iweathermap_backend python manage.py migrate
docker exec iweathermap_backend python manage.py loaddata forecast/fixtures/01_city.json

# Change the sentry dns settings in .env file
# https://sentry.io
SENTRY_DNS=https://xxxxxxxx@xxxx.ingest.sentry.io/xxxxx

# Running in development mode
docker exec -it iweathermap_backend python manage.py runserver 0:8000

# Deployment to docker swarm
docker stack deploy -c <(docker-compose -f docker-compose-swarm.yml config) iweathermap

```

### Running tests
```bash

docker exec -it iweathermap_backend ./test.sh

```

### Running lint based on Google Style Guide in development mode
```bash

# run lint on project
docker exec -it iweathermap_backend ./lint.sh

```

### Mini Challenge 
```python

# Run Python on docker
docker exec -it iweathermap_backend python

# Copy and past the following code
from core.openweathermap import OpenWeatherMap

cl = OpenWeatherMap(
    city_id="3451328",
    timezone="America/Sao_Paulo",
    api_key="Your-OpenWeatherMap-Key")

cl.display_raining_days()

# Should display something just like this
> "You should take an umbrella in these days: Tuesday, Wednesday and Sunday"
```

## Features

### Forecast

- [x] Get next five days with every 3 hour data
- [x] City list

### Audit
- [x] Tracking application error (Sentry)

### Docker and Swarm
- [x] Dockerize project
- [x] Swarm mode
