This is some experimentation with PostGIS and GeoDjango.

## Quick start

Build the containers and start a bash shell in one of them:

```
docker-compose run app bash
```

Then, once inside the shell, run:

```
python manage.py migrate
```

Then exit the shell and start everything up:

```
exit
docker-compose up
```

Then visit http://localhost:8000.
