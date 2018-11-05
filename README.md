This is some experimentation with PostGIS and GeoDjango.

## Quick start

First create an `.env` file:

```
cp .env.sample .env
```

Now edit it as needed.

Then build the containers and start a bash shell in one of them:

```
docker-compose run app bash
```

Then, once inside the shell, run:

```
python manage.py migrate
python manage.py loadworld
python manage.py loadnyc
```

Then exit the shell and start everything up:

```
exit
docker-compose up
```

Then visit http://localhost:8000.

## JavaScript typings

There's a `package.json` in the root directory, but it's optional, as it just
includes optional typings for use with TypeScript's JS checking mode.

## Data provenance

Data was originally exported from the following sources.

* `nyc/data/ZIP_CODE_040114` - https://data.cityofnewyork.us/Business/Zip-Code-Boundaries/i8iw-xf4u
* `nyc/data/Borough-Boundaries.geojson` - https://data.cityofnewyork.us/City-Government/Borough-Boundaries/tqmj-j8zm
* `nyc/data/Community-Districts.geojson` - https://data.cityofnewyork.us/City-Government/Community-Districts/yfnk-k7r4
* `nyc/data/ZillowNeighborhoods-NY` - https://www.zillow.com/howto/api/neighborhood-boundaries.htm
* `world/data` - http://thematicmapping.org/downloads/world_borders.php
