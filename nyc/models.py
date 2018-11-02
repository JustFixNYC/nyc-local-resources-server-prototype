from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.db.models.functions import Distance

from . import geocoding


class Zipcode(models.Model):
    class Meta:
        ordering = ['zipcode']

    zipcode = models.CharField(max_length=5, primary_key=True)
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.zipcode


zipcode_mapping = {
    'zipcode': 'ZIPCODE',
    'geom': 'POLYGON',
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
        for zipcode in self.zipcodes.all():
            total_area = total_area.union(zipcode.geom)
        self.catchment_area = total_area

    def save(self, *args, **kwargs):
        if self.address != self.geocoded_address or not self.geocoded_point:
            self.update_geocoded_info()
        super().save(*args, **kwargs)
