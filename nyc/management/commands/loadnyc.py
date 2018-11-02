from pathlib import Path
from collections import defaultdict
from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Polygon

from nyc import models
from nyc.models import Zipcode, Borough, Neighborhood


DATA_DIR = Path(models.__file__).parent.resolve() / 'data'
ZIPCODE_SHAPEFILE = DATA_DIR / 'ZIP_CODE_040114' / 'ZIP_CODE_040114.shp'
BOROUGH_SHAPEFILE = DATA_DIR / 'Borough-Boundaries.geojson'
NEIGHBORHOOD_SHAPEFILE = DATA_DIR / 'ZillowNeighborhoods-NY' / 'ZillowNeighborhoods-NY.shp'

def get_or_construct(model, **kwargs):
    instance = model.objects.filter(**kwargs).first()
    if instance is None:
        instance = model(**kwargs)
    return instance


def to_multipolygon(geos_geom):
    if isinstance(geos_geom, Polygon):
        return MultiPolygon(geos_geom)
    assert isinstance(geos_geom, MultiPolygon)
    return geos_geom


class Command(BaseCommand):
    help = 'Loads NYC geographic data into the database.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.load_zipcodes()
        self.load_neighborhoods()
        self.load_boroughs()

    def load_neighborhoods(self):
        ds = DataSource(str(NEIGHBORHOOD_SHAPEFILE))
        layer = ds[0]
        nyc_features = [
            feature for feature in layer
            if str(feature['City']) == 'New York'
        ]
        # The same neighborhoods are present multiple times
        # in different counties, but they cover the same
        # geographic areas and have the same names, so we'll
        # coalesce them.
        #
        # We'll use the "RegionID" for this, which represents
        # the shape of the area. This allows us to disambiguate
        # between neighborhoods in different counties with the
        # same name that actually *do* represent different
        # geographic areas, like Murray Hill.
        region_counties = defaultdict(list)
        for feature in nyc_features:
            region = str(feature['RegionID'])
            region_counties[region].append(str(feature['County']))
        regions = set()
        for feature in nyc_features:
            region = str(feature['RegionID'])
            if region in regions:
                continue
            regions.add(region)
            name = str(feature['Name'])
            county = ' / '.join(region_counties[region])
            instance = get_or_construct(
                Neighborhood,
                name=name,
                county=county
            )
            geom = feature.geom
            geom.transform(4326)
            instance.geom = to_multipolygon(geom.geos)
            print(f"Saving neighborhood {instance}.")
            instance.save()

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
            instance.geom = to_multipolygon(geos_geom)
            instance.save()
        print(f"Loaded {len(zipcodes)} zipcodes across {len(layer)} features.")
