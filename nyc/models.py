from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.db.models.functions import Distance

from . import geocoding


# This was originally created with:
#
# python manage.py ogrinspect --mapping --srid=4326 --multi \
#   nyc/data/nyc_zipcodes/nyc_zipcodes.shp Zipcode

class Zipcode(models.Model):
    class Meta:
        ordering = ['postalcode']

    st_fips = models.CharField(max_length=2)
    bldgpostal = models.IntegerField()
    objectid = models.IntegerField()
    id_url = models.CharField(max_length=52)
    cty_fips = models.CharField(max_length=3)
    cartodb_id = models.IntegerField()
    borough = models.CharField(max_length=13)
    state = models.CharField(max_length=2)
    po_name = models.CharField(max_length=19)
    postalcode = models.CharField(max_length=5)
    latitude = models.FloatField()
    longitude = models.FloatField()

    # TODO: I don't actually know if this needs to
    # be a MultiPolygonField, but I decided to use it
    # instead of a PolygonField just in case.
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.postalcode


zipcode_mapping = {
    'st_fips': 'st_fips',
    'bldgpostal': 'bldgpostal',
    'objectid': 'objectid',
    'id_url': 'id',
    'cty_fips': 'cty_fips',
    'cartodb_id': 'cartodb_id',
    'borough': 'borough',
    'state': 'state',
    'po_name': 'po_name',
    'postalcode': 'postalcode',
    'latitude': 'latitude',
    'longitude': 'longitude',
    'geom': 'MULTIPOLYGON',
}


class TenantResourceManager(models.Manager):
    def find_best_for(self, latitude: float, longitude: float):
        origin = Point(longitude, latitude, srid=4326)
        return self.filter(
            catchment_area__contains=Point(longitude, latitude),
        ).annotate(distance=Distance('geocoded_point', origin)).order_by('distance')


class TenantResource(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    zipcodes = models.ManyToManyField(Zipcode)

    geocoded_address = models.TextField(blank=True)
    geocoded_latitude = models.FloatField(default=0.0)
    geocoded_longitude = models.FloatField(default=0.0)
    geocoded_point = models.PointField(null=True, blank=True, srid=4326)
    catchment_area = models.MultiPolygonField(null=True, blank=True, srid=4326)

    objects = TenantResourceManager()

    def __str__(self):
        return self.name

    def update_geocoded_info(self):
        results = geocoding.search(self.address)
        if results:
            result = results[0]
            self.geocoded_address = result.properties.label
            longitude, latitude = result.geometry.coordinates
            self.geocoded_latitude = latitude
            self.geocoded_longitude = longitude
            self.geocoded_point = Point(longitude, latitude)

    def update_catchment_area(self):
        total_area = GEOSGeometry('POINT EMPTY', srid=4326)
        postalcodes = [z.postalcode for z in self.zipcodes.all()]
        for zipcode in Zipcode.objects.filter(postalcode__in=postalcodes):
            total_area = total_area.union(zipcode.geom)
        self.catchment_area = total_area

    def save(self, *args, **kwargs):
        if self.address != self.geocoded_address or not self.geocoded_point:
            self.update_geocoded_info()
        super().save(*args, **kwargs)
