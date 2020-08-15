# IWeatherMap - A Python and Django API for Weather Notification

## Development Installation and Deployment to Docker Swarm

```bash

# Clone de repository
git clone https://github.com/gustavo-fonseca/iweathermap

# Go to project`s folder and copy .env.example to .env
cd ./iweathermap
cp .env.example .env

# Run docker-compose and make the initial migrations
docker-compose up -d
docker exec store_backend python manage.py makemigrations
docker exec store_backend python manage.py migrate

# Change the email credentials settings in .env file
# Use sendgrid.net or other smtp service
EMAIL_USE_TLS=True
EMAIL_HOST=smtp.sendgrid.net
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=YOUR_KEY
EMAIL_PORT=587

# Change the sentry dns settings in .env file
# https://sentry.io
SENTRY_DNS=https://xxxxxxxx@xxxx.ingest.sentry.io/xxxxx

# Or use email backend console for dev mode in settings.py file
# (Only if the email credentials were not provided)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Running tests
docker exec iweathermap_backend python manage.py test

# Running in development mode
docker exec -it iweathermap_backend python manage.py runserver 0:8000


```

### Running lint based on Google Style Guide
```bash
# install pylint
pip install pylint

# run lint on project
find . -name "*.py" -and -not -name "0*.py" | xargs pylint
```

## Features

- [x] Get next five days forecast with 3 hour data
- [x] Get next five days forecast with max humidity data
- [x] Get next few days with rain changes


### Email Queue
- [ ] Redis queue to send email

### Audit
- [ ] Tracking application error (Sentry)

### CI/CD
- [ ] Drone CI

### Media/Static files storage
- [ ] AWS S3

### Docker and Swarm
- [x] Dockerize project
- [ ] Swarm mode
