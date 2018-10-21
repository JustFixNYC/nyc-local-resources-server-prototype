from django.contrib.gis.db import models

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
