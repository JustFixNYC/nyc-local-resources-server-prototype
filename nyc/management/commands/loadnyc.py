from pathlib import Path
from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Polygon

from nyc import models
from nyc.models import Zipcode, Borough


DATA_DIR = Path(models.__file__).parent.resolve() / 'data'
ZIPCODE_SHAPEFILE = DATA_DIR / 'ZIP_CODE_040114' / 'ZIP_CODE_040114.shp'
BOROUGH_SHAPEFILE = DATA_DIR / 'Borough-Boundaries.geojson'

def get_or_construct(model, **kwargs):
    instance = model.objects.filter(**kwargs).first()
    if instance is None:
        instance = model(**kwargs)
    return instance


class Command(BaseCommand):
    help = 'Loads NYC geographic data into the database.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.load_zipcodes()
        self.load_boroughs()

    def load_boroughs(self):
        ds = DataSource(str(BOROUGH_SHAPEFILE))
        layer = ds[0]
        for feature in layer:
            code = int(str(feature['boro_code']))
            name = str(feature['boro_name'])
            geom = feature.geom
            geom.transform(4326)
            instance = get_or_construct(Borough, code=code)
            instance.name = name
            instance.geom = geom.geos
            print(f"Saving borough {name}.")
            instance.save()

    def load_zipcodes(self):
        ds = DataSource(str(ZIPCODE_SHAPEFILE))
        layer = ds[0]
        zipcodes = {}
        for feature in layer:
            zipcode = str(feature['ZIPCODE'])
            geom = feature.geom
            geom.transform(4326)
            if zipcode in zipcodes:
                zipcodes[zipcode] = zipcodes[zipcode].union(geom.geos)
            else:
                zipcodes[zipcode] = geom.geos
        for zipcode, geos_geom in zipcodes.items():
            print(f"Saving zipcode {zipcode}.")
            instance = get_or_construct(Zipcode, zipcode=zipcode)
            if isinstance(geos_geom, Polygon):
                geos_geom = MultiPolygon(geos_geom)
            instance.geom = geos_geom
            instance.save()
        print(f"Loaded {len(zipcodes)} zipcodes across {len(layer)} features.")
