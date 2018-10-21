from pathlib import Path
from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping

from nyc import models


DATA_DIR = Path(models.__file__).parent.resolve() / 'data'
ZIPCODE_SHAPEFILE = DATA_DIR / 'nyc_zipcodes' / 'nyc_zipcodes.shp'

class Command(BaseCommand):
    help = 'Loads NYC geographic data into the database.'

    def handle(self, *args, **options):
        lm = LayerMapping(
            models.Zipcode,
            str(ZIPCODE_SHAPEFILE),
            models.zipcode_mapping,
            transform=False
        )
        lm.save(strict=True, verbose=True)
